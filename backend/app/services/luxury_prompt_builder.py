from __future__ import annotations

from app.models.schemas import GenerateRequest, JewelleryType


STYLE_MAP = {
    "signature_minimal": "delicate refined high-jewellery",
    "evening_elegance": "elegant radiant evening luxury",
    "bridal_heirloom": "ornate heirloom bridal craftsmanship",
    "contemporary_couture": "sleek modern high-fashion jewellery",
}


class LuxuryPromptBuilder:
    def build(self, request: GenerateRequest) -> str:
        style_descriptor = STYLE_MAP[request.style.value]
        variant_phrase = f" with a {request.variant.replace('_', ' ')} silhouette" if request.variant else ""

        if request.jewelleryType == JewelleryType.earrings:
            return (
                f"Add realistic premium {request.metal.value.replace('_', ' ')} earrings featuring "
                f"{request.stone.value} stones in a {style_descriptor} luxury design{variant_phrase}. "
                "Align naturally with the visible ears and face angle. Preserve identity, skin texture, "
                "hairstyle, clothing, and background. Do not alter any other part of the image."
            )
        if request.jewelleryType == JewelleryType.necklace:
            return (
                f"Add a realistic premium {request.metal.value.replace('_', ' ')} necklace featuring "
                f"{request.stone.value} details in a {style_descriptor} luxury design{variant_phrase} "
                "around the neck with natural drape, shadow, and scale. Preserve identity, outfit, "
                "body shape, and background. Do not alter any other part of the image."
            )
        if request.jewelleryType == JewelleryType.nose_pin:
            side = request.placement.side or "left"
            return (
                f"Add a realistic premium {request.metal.value.replace('_', ' ')} nose pin featuring "
                f"{request.stone.value} detail on the {side} nostril in a {style_descriptor} style. "
                "Preserve facial identity, skin tone, hair, makeup, and background. Do not alter any other part of the image."
            )
        return (
            f"Add a realistic premium {request.metal.value.replace('_', ' ')} ring featuring "
            f"{request.stone.value} detail on the selected finger in a {style_descriptor} luxury design{variant_phrase}. "
            "Use correct perspective, wrapping, reflections, and scale. Preserve hand shape, skin tone, "
            "nails, and background. Do not alter any other part of the image."
        )
