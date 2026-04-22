from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import cv2
import numpy as np
from PIL import Image, ImageOps

from app.core.config import get_settings
from app.utils.errors import ValidationError


@dataclass
class ValidationResult:
    width: int
    height: int
    warnings: List[str]
    auto_upscaled: bool = False


class ImageValidationService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def validate_or_raise(self, path: Path) -> ValidationResult:
        image = Image.open(path).convert("RGB")
        width, height = image.size
        warnings: List[str] = []
        auto_upscaled = False
        if width < self.settings.min_image_width or height < self.settings.min_image_height:
            if width < self.settings.min_recoverable_width or height < self.settings.min_recoverable_height:
                raise ValidationError("Portrait resolution is too low for premium jewellery placement.")
            image, width, height = self._recover_resolution(image, path)
            auto_upscaled = True
            warnings.append("Your portrait was gently optimized for placement clarity before analysis.")

        array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        blur_variance = cv2.Laplacian(array, cv2.CV_64F).var()
        if blur_variance < self.settings.max_blur_variance:
            warnings.append("The portrait appears soft. Fine jewellery edges may be less precise.")

        return ValidationResult(width=width, height=height, warnings=warnings, auto_upscaled=auto_upscaled)

    def _recover_resolution(self, image: Image.Image, path: Path) -> tuple[Image.Image, int, int]:
        target_width = max(self.settings.min_image_width, image.width)
        target_height = max(self.settings.min_image_height, image.height)
        recovered = ImageOps.contain(image, (target_width, target_height), method=Image.Resampling.LANCZOS)
        if recovered.size != (target_width, target_height):
            recovered = recovered.resize((target_width, target_height), Image.Resampling.LANCZOS)
        recovered.save(path)
        return recovered, recovered.width, recovered.height
