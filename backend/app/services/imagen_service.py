from __future__ import annotations

import logging
import tempfile
import uuid
from io import BytesIO
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from app.core.config import get_settings
from app.models.schemas import GenerateRequest
from app.services.landmark_service import LandmarkAnalysis
from app.services.result_postprocess import ResultPostprocessService
from app.utils.errors import ProviderUnavailableError

logger = logging.getLogger(__name__)


@dataclass
class EditResult:
    image: Image.Image


class ImageEditorProvider:
    def edit_image(
        self,
        original_path: Path,
        mask: Image.Image,
        prompt: str,
        request: GenerateRequest,
        analysis: LandmarkAnalysis,
    ) -> List[EditResult]:
        raise NotImplementedError


class VertexImagenEditor(ImageEditorProvider):
    def __init__(self) -> None:
        self.settings = get_settings()

    def is_ready(self) -> bool:
        return bool(
            self.settings.google_cloud_project
            and self.settings.google_cloud_location
            and self.settings.vertex_imagen_edit_model
        )

    def edit_image(
        self,
        original_path: Path,
        mask: Image.Image,
        prompt: str,
        request: GenerateRequest,
        analysis: LandmarkAnalysis,
    ) -> List[EditResult]:
        if not self.is_ready():
            raise ProviderUnavailableError("Vertex Imagen configuration is incomplete.")

        if self.settings.vertex_imagen_edit_model.startswith("gemini-"):
            return self._edit_with_gemini(original_path, mask, prompt, request)

        return self._edit_with_imagen(original_path, mask, prompt, request)

    def _edit_with_imagen(
        self,
        original_path: Path,
        mask: Image.Image,
        prompt: str,
        request: GenerateRequest,
    ) -> List[EditResult]:
        try:
            import vertexai
            from vertexai.preview.vision_models import Image as VertexImage
            from vertexai.preview.vision_models import ImageGenerationModel
        except ImportError as exc:  # pragma: no cover
            raise ProviderUnavailableError("Vertex AI SDK is not installed in this runtime.") from exc

        mask_path = Path(tempfile.gettempdir()) / f"{uuid.uuid4().hex}-mask.png"
        mask.convert("RGB").save(mask_path, format="PNG")

        try:
            vertexai.init(
                project=self.settings.google_cloud_project,
                location=self.settings.google_cloud_location,
            )
            model = ImageGenerationModel.from_pretrained(self.settings.vertex_imagen_edit_model)
            base_img = VertexImage.load_from_file(location=str(original_path))
            mask_img = VertexImage.load_from_file(location=str(mask_path))
            guidance_scale = self._guidance_scale_for(request)
            edited_images = model.edit_image(
                base_image=base_img,
                mask=mask_img,
                prompt=prompt,
                guidance_scale=guidance_scale,
                number_of_images=request.variants,
            )
        except Exception as exc:  # pragma: no cover
            raise ProviderUnavailableError(f"Vertex Imagen edit request failed: {exc}") from exc
        finally:
            mask_path.unlink(missing_ok=True)

        outputs: List[EditResult] = []
        for index, generated in enumerate(edited_images):
            temp_output = Path(tempfile.gettempdir()) / f"{uuid.uuid4().hex}-{index}.png"
            try:
                generated.save(location=str(temp_output), include_generation_parameters=False)
                rendered = Image.open(temp_output).convert("RGB")
                outputs.append(EditResult(image=rendered.copy()))
            finally:
                if temp_output.exists():
                    temp_output.unlink()

        if not outputs:
            raise ProviderUnavailableError("Vertex Imagen returned no edited images.")

        return outputs

    def _edit_with_gemini(
        self,
        original_path: Path,
        mask: Image.Image,
        prompt: str,
        request: GenerateRequest,
    ) -> List[EditResult]:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:  # pragma: no cover
            raise ProviderUnavailableError("Google Gen AI SDK is not installed in this runtime.") from exc

        original_image = Image.open(original_path).convert("RGB")
        mask_hint = self._mask_hint_image(original_image.size, mask)
        client = genai.Client(
            vertexai=True,
            project=self.settings.google_cloud_project,
            location=self.settings.google_cloud_location or "global",
        )

        instruction = (
            f"{prompt} Use the second image as a strict edit mask guide: only modify the white highlighted region, "
            "keep all other pixels unchanged, and produce a realistic luxury jewellery edit with natural materials, "
            "shadow, perspective, and reflections."
        )

        outputs: List[EditResult] = []
        for index in range(request.variants):
            seed = (abs(hash((request.image_id, request.jewelleryType.value, request.style.value, index))) % 10_000_000) + 1
            try:
                response = client.models.generate_content(
                    model=self.settings.vertex_imagen_edit_model,
                    contents=[original_image, mask_hint, instruction],
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        seed=seed,
                    ),
                )
            except Exception as exc:  # pragma: no cover
                raise ProviderUnavailableError(f"Gemini image edit request failed: {exc}") from exc

            rendered = self._extract_gemini_image(response)
            if rendered is None:
                raise ProviderUnavailableError("Gemini image edit returned no image content.")
            outputs.append(EditResult(image=rendered.convert("RGB")))

        return outputs

    @staticmethod
    def _mask_hint_image(size: tuple[int, int], mask: Image.Image) -> Image.Image:
        grayscale = mask.convert("L").resize(size)
        rgba = Image.new("RGBA", size, (0, 0, 0, 255))
        rgba.putalpha(grayscale)
        overlay = Image.new("RGBA", size, (255, 255, 255, 0))
        overlay.putalpha(grayscale)
        return Image.alpha_composite(rgba, overlay).convert("RGB")

    @staticmethod
    def _extract_gemini_image(response: object) -> Image.Image | None:
        parts = getattr(response, "parts", None)
        if parts:
            for part in parts:
                image = VertexImagenEditor._image_from_part(part)
                if image is not None:
                    return image

        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            candidate_parts = getattr(content, "parts", None) or []
            for part in candidate_parts:
                image = VertexImagenEditor._image_from_part(part)
                if image is not None:
                    return image
        return None

    @staticmethod
    def _image_from_part(part: object) -> Image.Image | None:
        as_image = getattr(part, "as_image", None)
        if callable(as_image):
            try:
                return as_image()
            except Exception:
                pass

        inline_data = getattr(part, "inline_data", None)
        if inline_data is None:
            return None

        data = getattr(inline_data, "data", None)
        if data is None and isinstance(inline_data, dict):
            data = inline_data.get("data")
        if data is None:
            return None

        if isinstance(data, str):
            import base64

            raw = base64.b64decode(data)
        else:
            raw = data

        return Image.open(BytesIO(raw))

    @staticmethod
    def _guidance_scale_for(request: GenerateRequest) -> int:
        if request.scale.value == "refined":
            return 18
        if request.scale.value == "statement":
            return 20
        return 22


class FallbackPreviewEditor(ImageEditorProvider):
    def __init__(self) -> None:
        self.postprocess = ResultPostprocessService()

    def edit_image(
        self,
        original_path: Path,
        mask: Image.Image,
        prompt: str,
        request: GenerateRequest,
        analysis: LandmarkAnalysis,
    ) -> List[EditResult]:
        base = Image.open(original_path).convert("RGBA")
        mask = mask.convert("L")
        outputs: List[EditResult] = []
        palette = [
            ((226, 193, 107, 215), (255, 255, 255, 210)),
            ((214, 226, 235, 215), (189, 234, 255, 210)),
            ((232, 184, 173, 215), (255, 224, 220, 210)),
        ]

        for index in range(request.variants):
            gold, highlight = palette[index % len(palette)]
            overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            mask_array = np.array(mask)
            ys, xs = np.where(mask_array > 10)
            if len(xs) == 0 or len(ys) == 0:
                outputs.append(EditResult(image=base.convert("RGB")))
                continue
            x1, y1, x2, y2 = xs.min(), ys.min(), xs.max(), ys.max()
            self._paint_jewellery(
                overlay_draw,
                mask,
                request,
                analysis,
                gold,
                highlight,
                (x1, y1, x2, y2),
                index,
            )
            sparkle = Image.new("RGBA", base.size, (0, 0, 0, 0))
            sparkle_draw = ImageDraw.Draw(sparkle)
            if request.jewelleryType.value != "necklace":
                sparkle_draw.ellipse((x1, y1, x2, y2), outline=highlight, width=max(2, (x2 - x1) // 14))
            overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.4))
            composite = Image.alpha_composite(base, overlay)
            composite = Image.alpha_composite(composite, sparkle)
            outputs.append(EditResult(image=self.postprocess.refine(composite.convert("RGB"))))
        return outputs

    def _paint_jewellery(
        self,
        draw: ImageDraw.ImageDraw,
        mask: Image.Image,
        request: GenerateRequest,
        analysis: LandmarkAnalysis,
        metal: tuple[int, int, int, int],
        highlight: tuple[int, int, int, int],
        box: tuple[int, int, int, int],
        variant_index: int,
    ) -> None:
        x1, y1, x2, y2 = box
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        width = max(12.0, x2 - x1)
        height = max(12.0, y2 - y1)

        if request.jewelleryType.value == "necklace":
            neck_x, neck_y = analysis.anchors["neck_center"]
            chest_x, chest_y = analysis.anchors["chest_center"]
            face_width = analysis.faces[0].box.width if analysis.faces else width * 0.6
            half_width = max(46.0, min(face_width * 0.42, width * 0.42))
            arc_top = neck_y - face_width * 0.05
            arc_bottom = chest_y + face_width * 0.18
            arc_box = (neck_x - half_width, arc_top, neck_x + half_width, arc_bottom)
            stroke = max(5, int(face_width * 0.03))
            draw.arc(arc_box, start=204, end=336, fill=metal, width=stroke)
            draw.arc(
                (
                    arc_box[0] + stroke * 0.7,
                    arc_box[1] + stroke * 0.9,
                    arc_box[2] - stroke * 0.7,
                    arc_box[3] - stroke * 0.7,
                ),
                start=208,
                end=332,
                fill=highlight,
                width=max(2, stroke // 3),
            )
            if request.variant in {"pendant", "solitaire_drop", "bridal_set"}:
                pendant_w = max(16.0, face_width * 0.08)
                pendant_h = max(20.0, face_width * 0.11)
                pendant_top = chest_y - pendant_h * 0.45 + (variant_index * 2.0)
                pendant_box = (
                    chest_x - pendant_w / 2,
                    pendant_top,
                    chest_x + pendant_w / 2,
                    pendant_top + pendant_h,
                )
                draw.ellipse(pendant_box, fill=metal)
                inner = 2 if pendant_w < 20 else 3
                draw.ellipse(
                    (
                        pendant_box[0] + inner,
                        pendant_box[1] + inner,
                        pendant_box[2] - inner,
                        pendant_box[3] - inner,
                    ),
                    outline=highlight,
                    width=max(2, inner),
                )
            return

        if request.jewelleryType.value == "ring":
            stroke = max(5, int(height * 0.4))
            draw.ellipse((x1, y1, x2, y2), outline=metal, width=stroke)
            draw.ellipse(
                (x1 + stroke * 0.35, y1 + stroke * 0.2, x2 - stroke * 0.35, y2 - stroke * 0.2),
                outline=highlight,
                width=max(2, stroke // 3),
            )
            return

        if request.jewelleryType.value == "nose_pin":
            draw.ellipse((x1, y1, x2, y2), fill=metal)
            inset = max(2, int(min(width, height) * 0.2))
            draw.ellipse((x1 + inset, y1 + inset, x2 - inset, y2 - inset), fill=highlight)
            return

        draw.bitmap((0, 0), mask, fill=metal)
        accent = max(2, int(min(width, height) * 0.12))
        draw.ellipse((x1 + accent, y1 + accent, x2 - accent, y2 - accent), outline=highlight, width=max(2, accent // 2))


class ImagenService:
    def __init__(self) -> None:
        self.vertex = VertexImagenEditor()
        self.fallback = FallbackPreviewEditor()

    def provider_status(self) -> dict[str, bool]:
        return {
            "vertexConfigured": self.vertex.is_ready(),
            "fallbackPreviewEnabled": True,
        }

    def generate(
        self,
        original_path: Path,
        mask: Image.Image,
        prompt: str,
        request: GenerateRequest,
        analysis: LandmarkAnalysis,
    ) -> List[EditResult]:
        if self.vertex.is_ready():
            return self.vertex.edit_image(original_path, mask, prompt, request, analysis)

        logger.warning("Vertex provider unavailable; using local preview renderer.")
        return self.fallback.edit_image(original_path, mask, prompt, request, analysis)
