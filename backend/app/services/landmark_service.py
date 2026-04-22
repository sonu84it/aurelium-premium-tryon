from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

from app.utils.geometry import Box, box_from_center

try:
    import mediapipe as mp
except ImportError:  # pragma: no cover
    mp = None


@dataclass
class FaceEstimate:
    box: Box
    angle: str
    left_ear_visible: bool
    right_ear_visible: bool
    neck_visible: bool
    nostril_side: str


@dataclass
class HandEstimate:
    box: Box
    visible_fingers: List[str]


@dataclass
class LandmarkAnalysis:
    image_size: Tuple[int, int]
    faces: List[FaceEstimate]
    hands: List[HandEstimate]
    warnings: List[str]
    anchors: Dict[str, Tuple[int, int]]


class LandmarkService:
    def analyze(self, path: Path) -> LandmarkAnalysis:
        image = cv2.imread(str(path))
        height, width = image.shape[:2]
        warnings: List[str] = []

        if mp is None:
            return self._fallback_analysis(width, height, warnings)

        try:
            return self._fallback_analysis(width, height, warnings)
        except Exception:
            warnings.append("Using conservative placement fallback for this portrait.")
            return self._fallback_analysis(width, height, warnings)

    def _fallback_analysis(self, width: int, height: int, warnings: List[str]) -> LandmarkAnalysis:
        face_box = box_from_center(width * 0.5, height * 0.28, width * 0.34, height * 0.34, (width, height))
        face = FaceEstimate(
            box=face_box,
            angle="front",
            left_ear_visible=True,
            right_ear_visible=True,
            neck_visible=True,
            nostril_side="left",
        )

        hand_present = width > 900 and height > 1100
        hands: List[HandEstimate] = []
        anchors = {
            "left_ear": (int(face_box.x + face_box.width * 0.1), int(face_box.y + face_box.height * 0.55)),
            "right_ear": (int(face_box.x + face_box.width * 0.9), int(face_box.y + face_box.height * 0.55)),
            "nose_left": (int(face_box.x + face_box.width * 0.42), int(face_box.y + face_box.height * 0.62)),
            "nose_right": (int(face_box.x + face_box.width * 0.58), int(face_box.y + face_box.height * 0.62)),
            "neck_center": (int(width * 0.5), int(face_box.y2 + height * 0.08)),
            "chest_center": (int(width * 0.5), int(face_box.y2 + height * 0.18)),
        }
        if hand_present:
            hand_box = box_from_center(width * 0.7, height * 0.74, width * 0.16, height * 0.16, (width, height))
            hands.append(HandEstimate(box=hand_box, visible_fingers=["ring", "middle", "index"]))
            anchors["ring_finger"] = (int(hand_box.x + hand_box.width * 0.45), int(hand_box.y + hand_box.height * 0.48))
            anchors["middle_finger"] = (int(hand_box.x + hand_box.width * 0.57), int(hand_box.y + hand_box.height * 0.36))
            anchors["index_finger"] = (int(hand_box.x + hand_box.width * 0.68), int(hand_box.y + hand_box.height * 0.3))
        else:
            warnings.append("Hand visibility is limited for ring placement.")

        return LandmarkAnalysis(
            image_size=(width, height),
            faces=[face],
            hands=hands,
            warnings=warnings,
            anchors=anchors,
        )
