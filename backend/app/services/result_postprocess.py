from __future__ import annotations

from PIL import Image, ImageEnhance


class ResultPostprocessService:
    def refine(self, image: Image.Image) -> Image.Image:
        image = image.convert("RGB")
        image = ImageEnhance.Sharpness(image).enhance(1.08)
        image = ImageEnhance.Contrast(image).enhance(1.03)
        return image
