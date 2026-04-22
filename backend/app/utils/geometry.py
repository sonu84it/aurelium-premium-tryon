from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


@dataclass
class Box:
    x: int
    y: int
    width: int
    height: int

    @property
    def x2(self) -> int:
        return self.x + self.width

    @property
    def y2(self) -> int:
        return self.y + self.height

    def as_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x, self.y, self.x2, self.y2)


def clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(value, upper))


def box_from_center(cx: float, cy: float, width: float, height: float, image_size: Tuple[int, int]) -> Box:
    image_width, image_height = image_size
    x = clamp(int(cx - width / 2), 0, image_width - 1)
    y = clamp(int(cy - height / 2), 0, image_height - 1)
    x2 = clamp(int(cx + width / 2), 0, image_width)
    y2 = clamp(int(cy + height / 2), 0, image_height)
    return Box(x=x, y=y, width=max(1, x2 - x), height=max(1, y2 - y))


def merge_boxes(boxes: Iterable[Box], image_size: Tuple[int, int]) -> Box:
    boxes = list(boxes)
    if not boxes:
        return Box(0, 0, image_size[0], image_size[1])
    x1 = min(box.x for box in boxes)
    y1 = min(box.y for box in boxes)
    x2 = max(box.x2 for box in boxes)
    y2 = max(box.y2 for box in boxes)
    return Box(x1, y1, x2 - x1, y2 - y1)
