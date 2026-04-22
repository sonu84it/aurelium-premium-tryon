from app.models.schemas import GenerateRequest, JewelleryType, MetalType, ScaleType, StoneType, StyleType
from app.services.naming_service import NamingService


def test_naming_service_builds_premium_titles() -> None:
    request = GenerateRequest(
        image_id="img",
        jewelleryType=JewelleryType.ring,
        metal=MetalType.rose_gold,
        stone=StoneType.ruby,
        style=StyleType.bridal_heirloom,
        scale=ScaleType.grand,
    )
    title = NamingService().build_title(request, 0)
    assert title == "Ruby Signature Ring"
