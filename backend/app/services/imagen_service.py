from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from app.core.config import get_settings
from app.models.schemas import GenerateRequest
from app.services.result_postprocess import ResultPostprocessService
from app.utils.errors import ProviderUnavailableError

logger = logging.getLogger(__name__)


@dataclass
class EditResult:
    image: Image.Image


class ImageEditorProvider:
    def edit_image(self, original_path: Path, mask: Image.Image, prompt: str, variants: int) -> List[EditResult]:
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

    def edit_image(self, original_path: Path, mask: Image.Image, prompt: str, variants: int) -> List[EditResult]:
        if not self.is_ready():
            raise ProviderUnavailableError("Vertex Imagen configuration is incomplete.")

        raise ProviderUnavailableError(
            "Vertex Imagen editing is configured by env, but the runtime integration should be completed "
            "with project-specific credentials before production use."
        )


class FallbackPreviewEditor(ImageEditorProvider):
    def __init__(self) -> None:
        self.postprocess = ResultPostprocessService()

    def edit_image(self, original_path: Path, mask: Image.Image, prompt: str, variants: int) -> List[EditResult]:
        base = Image.open(original_path).convert("RGBA")
        mask = mask.convert("L")
        outputs: List[EditResult] = []
        palette = [
            ((226, 193, 107, 215), (255, 255, 255, 210)),
            ((214, 226, 235, 215), (189, 234, 255, 210)),
            ((232, 184, 173, 215), (255, 224, 220, 210)),
        ]

        for index in range(variants):
            gold, highlight = palette[index % len(palette)]
            overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            mask_array = np.array(mask)
            ys, xs = np.where(mask_array > 10)
            if len(xs) == 0 or len(ys) == 0:
                outputs.append(EditResult(image=base.convert("RGB")))
                continue
            x1, y1, x2, y2 = xs.min(), ys.min(), xs.max(), ys.max()
            overlay_draw.bitmap((0, 0), mask, fill=gold)
            sparkle = Image.new("RGBA", base.size, (0, 0, 0, 0))
            sparkle_draw = ImageDraw.Draw(sparkle)
            sparkle_draw.ellipse((x1, y1, x2, y2), outline=highlight, width=max(2, (x2 - x1) // 14))
            overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.4))
            composite = Image.alpha_composite(base, overlay)
            composite = Image.alpha_composite(composite, sparkle)
            outputs.append(EditResult(image=self.postprocess.refine(composite.convert("RGB"))))
        return outputs


class ImagenService:
    def __init__(self) -> None:
        self.vertex = VertexImagenEditor()
        self.fallback = FallbackPreviewEditor()

    def provider_status(self) -> dict[str, bool]:
        return {
            "vertexConfigured": self.vertex.is_ready(),
            "fallbackPreviewEnabled": True,
        }

    def generate(self, original_path: Path, mask: Image.Image, prompt: str, request: GenerateRequest) -> List[EditResult]:
        try:
            return self.vertex.edit_image(original_path, mask, prompt, request.variants)
        except ProviderUnavailableError as exc:
            logger.warning("Falling back to preview renderer: %s", exc)
            return self.fallback.edit_image(original_path, mask, prompt, request.variants)
