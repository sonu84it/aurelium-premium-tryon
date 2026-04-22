from app.models.schemas import GenerateRequest, JewelleryType, MetalType, ScaleType, StoneType, StyleType
from app.services.landmark_service import FaceEstimate, HandEstimate, LandmarkAnalysis
from app.services.mask_service import MaskService
from app.utils.geometry import Box


def test_necklace_mask_has_nonzero_pixels() -> None:
    request = GenerateRequest(
        image_id="img",
        jewelleryType=JewelleryType.necklace,
        metal=MetalType.platinum,
        stone=StoneType.diamond,
        style=StyleType.evening_elegance,
        scale=ScaleType.statement,
        variant="pendant",
    )
    analysis = LandmarkAnalysis(
        image_size=(1000, 1400),
        faces=[FaceEstimate(Box(300, 120, 360, 360), "front", True, True, True, "left")],
        hands=[HandEstimate(Box(640, 900, 120, 160), ["ring"])],
        warnings=[],
        anchors={
            "neck_center": (500, 580),
            "chest_center": (500, 720),
        },
    )
    mask, _ = MaskService().build_mask(request, analysis)
    assert mask.getbbox() is not None


def test_necklace_mask_handles_float_geometry() -> None:
    request = GenerateRequest(
        image_id="img",
        jewelleryType=JewelleryType.necklace,
        metal=MetalType.yellow_gold,
        stone=StoneType.emerald,
        style=StyleType.signature_minimal,
        scale=ScaleType.refined,
        variant="collar",
    )
    analysis = LandmarkAnalysis(
        image_size=(913, 1287),
        faces=[FaceEstimate(Box(240, 120, 320, 320), "front", True, True, True, "left")],
        hands=[],
        warnings=[],
        anchors={
            "neck_center": (456, 566),
            "chest_center": (457, 702),
        },
    )
    mask, _ = MaskService().build_mask(request, analysis)
    assert mask.getbbox() is not None
