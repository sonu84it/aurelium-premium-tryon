from __future__ import annotations

from typing import Dict, List

from app.models.schemas import DetectedInfo, ZoneAvailability
from app.services.landmark_service import LandmarkAnalysis


class AvailabilityService:
    def evaluate(self, analysis: LandmarkAnalysis) -> tuple[Dict[str, ZoneAvailability], DetectedInfo, List[str]]:
        warnings = list(analysis.warnings)
        faces = len(analysis.faces)
        hands = len(analysis.hands)

        if faces != 1:
            unavailable = ZoneAvailability(
                available=False,
                confidence=0.0,
                reason="A single clearly framed portrait is required for refined placement.",
            )
            availability = {
                "nosePin": unavailable,
                "earrings": unavailable,
                "necklace": unavailable,
                "ring": unavailable,
            }
            return availability, DetectedInfo(faces=faces, hands=hands, faceAngle="unknown", neckVisible=False), warnings

        face = analysis.faces[0]
        availability = {
            "nosePin": ZoneAvailability(
                available=True,
                confidence=0.88,
                recommendation="Suitable for gemstone nose pin previews.",
            ),
            "earrings": ZoneAvailability(
                available=face.left_ear_visible or face.right_ear_visible,
                confidence=0.9 if face.left_ear_visible and face.right_ear_visible else 0.7,
                reason=None if (face.left_ear_visible or face.right_ear_visible) else "Ear visibility is limited by hair or pose.",
                recommendation="Suitable for diamond earrings." if (face.left_ear_visible or face.right_ear_visible) else None,
            ),
            "necklace": ZoneAvailability(
                available=face.neck_visible,
                confidence=0.86 if face.neck_visible else 0.35,
                reason=None if face.neck_visible else "The neckline is too covered for a natural necklace drape.",
                recommendation="Suitable for pendant necklace previews." if face.neck_visible else None,
            ),
            "ring": ZoneAvailability(
                available=hands > 0,
                confidence=0.79 if hands > 0 else 0.22,
                reason=None if hands > 0 else "Hand visibility is limited for ring placement.",
                recommendation="Suitable for premium ring placement." if hands > 0 else None,
            ),
        }

        detected = DetectedInfo(
            faces=faces,
            hands=hands,
            faceAngle=face.angle,
            neckVisible=face.neck_visible,
        )
        return availability, detected, warnings
