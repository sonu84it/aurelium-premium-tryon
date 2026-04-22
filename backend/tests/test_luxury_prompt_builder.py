from app.models.schemas import GenerateRequest, JewelleryType, MetalType, ScaleType, StoneType, StyleType
from app.services.luxury_prompt_builder import LuxuryPromptBuilder


def test_builds_earring_prompt() -> None:
    request = GenerateRequest(
        image_id="abc",
        jewelleryType=JewelleryType.earrings,
        metal=MetalType.yellow_gold,
        stone=StoneType.diamond,
        style=StyleType.signature_minimal,
        scale=ScaleType.refined,
        variant="studs",
    )
    prompt = LuxuryPromptBuilder().build(request)
    assert "yellow gold earrings" in prompt
    assert "diamond stones" in prompt
    assert "Preserve identity" in prompt
