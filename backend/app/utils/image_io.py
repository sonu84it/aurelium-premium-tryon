from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
from PIL import Image


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def image_to_array(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def array_to_image(array: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(array, cv2.COLOR_BGR2RGB))


def save_image(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def bytes_to_image(data: bytes) -> Image.Image:
    return Image.open(BytesIO(data)).convert("RGB")


def image_size(path: Path) -> Tuple[int, int]:
    image = Image.open(path)
    return image.size
