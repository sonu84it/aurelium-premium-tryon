from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import cv2
import numpy as np
from PIL import Image

from app.models.schemas import GenerateRequest, JewelleryType
from app.services.landmark_service import LandmarkAnalysis
from app.utils.geometry import Box, box_from_center


class MaskService:
    def build_mask(self, request: GenerateRequest, analysis: LandmarkAnalysis) -> tuple[Image.Image, Dict[str, Box]]:
        width, height = analysis.image_size
        mask = np.zeros((height, width), dtype=np.uint8)
        boxes: Dict[str, Box] = {}

        if request.jewelleryType == JewelleryType.earrings:
            size = self._scale_size(request.scale.value, base=height * 0.055)
            for key in ["left_ear", "right_ear"]:
                if key in analysis.anchors:
                    cx, cy = analysis.anchors[key]
                    box = box_from_center(cx, cy + size * 0.15, size * 0.7, size * 1.1, analysis.image_size)
                    cv2.ellipse(mask, (cx, cy), (int(size * 0.28), int(size * 0.42)), 0, 0, 360, 255, -1)
                    boxes[key] = box

        elif request.jewelleryType == JewelleryType.necklace:
            neck_x, neck_y = analysis.anchors["neck_center"]
            chest_x, chest_y = analysis.anchors["chest_center"]
            width_span = self._scale_size(request.scale.value, base=width * 0.22)
            thickness = self._scale_size(request.scale.value, base=height * 0.015)
            center = (int(neck_x), int(chest_y - thickness))
            axes = (max(1, int(width_span)), max(1, int(width_span * 0.42)))
            cv2.ellipse(mask, center, axes, 0, 205, 335, 255, thickness=max(6, int(thickness)))
            if request.variant in {"pendant", "solitaire_drop"}:
                cv2.circle(mask, (chest_x, chest_y + int(thickness * 1.8)), max(7, int(thickness * 1.4)), 255, -1)
            boxes["necklace"] = box_from_center(neck_x, chest_y, width_span * 2.1, width_span * 1.0, analysis.image_size)

        elif request.jewelleryType == JewelleryType.nose_pin:
            side = request.placement.side or analysis.faces[0].nostril_side
            anchor = analysis.anchors["nose_left"] if side == "left" else analysis.anchors["nose_right"]
            radius = int(self._scale_size(request.scale.value, base=height * 0.008))
            cv2.circle(mask, anchor, max(4, radius), 255, -1)
            boxes["nose_pin"] = box_from_center(anchor[0], anchor[1], radius * 3, radius * 3, analysis.image_size)

        elif request.jewelleryType == JewelleryType.ring:
            finger = request.placement.finger or "ring"
            anchor = analysis.anchors.get(f"{finger}_finger") or analysis.anchors.get("ring_finger")
            if anchor:
                ring_width = int(self._scale_size(request.scale.value, base=width * 0.028))
                ring_height = max(8, ring_width // 2)
                cv2.ellipse(mask, anchor, (ring_width, ring_height), -18, 0, 360, 255, thickness=max(4, ring_height // 2))
                boxes["ring"] = box_from_center(anchor[0], anchor[1], ring_width * 2.5, ring_height * 3.0, analysis.image_size)

        feathered = cv2.GaussianBlur(mask, (0, 0), sigmaX=4.0)
        return Image.fromarray(feathered), boxes

    def _scale_size(self, scale: str, base: float) -> float:
        multipliers = {"refined": 1.0, "statement": 1.25, "grand": 1.55}
        return base * multipliers.get(scale, 1.0)
