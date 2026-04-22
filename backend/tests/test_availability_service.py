from app.services.availability_service import AvailabilityService
from app.services.landmark_service import FaceEstimate, HandEstimate, LandmarkAnalysis
from app.utils.geometry import Box


def test_ring_unavailable_without_hands() -> None:
    analysis = LandmarkAnalysis(
        image_size=(1024, 1280),
        faces=[FaceEstimate(Box(200, 100, 300, 300), "front", True, True, True, "left")],
        hands=[],
        warnings=[],
        anchors={},
    )
    availability, detected, _warnings = AvailabilityService().evaluate(analysis)
    assert availability["ring"].available is False
    assert detected.faces == 1


def test_earrings_available_when_face_visible() -> None:
    analysis = LandmarkAnalysis(
        image_size=(1024, 1280),
        faces=[FaceEstimate(Box(200, 100, 300, 300), "front", True, False, True, "left")],
        hands=[HandEstimate(Box(600, 800, 120, 120), ["ring"])],
        warnings=[],
        anchors={},
    )
    availability, _detected, _warnings = AvailabilityService().evaluate(analysis)
    assert availability["earrings"].available is True
