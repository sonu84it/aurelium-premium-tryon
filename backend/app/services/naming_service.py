from __future__ import annotations

from app.models.schemas import GenerateRequest, JewelleryType, StoneType


STONE_PREFIX = {
    StoneType.diamond: "Diamond",
    StoneType.emerald: "Emerald",
    StoneType.ruby: "Ruby",
    StoneType.sapphire: "Sapphire",
}


TITLE_MAP = {
    JewelleryType.earrings: ["Solstice Studs", "Evening Drops", "Halo Hoops"],
    JewelleryType.necklace: ["Halo Pendant", "Drape Collar", "Heritage Set"],
    JewelleryType.nose_pin: ["Petite Halo Nose Pin", "Solitaire Bloom Nose Pin", "Floral Radiance Nose Pin"],
    JewelleryType.ring: ["Signature Ring", "Emerald Cut Ring", "Couture Halo Ring"],
}


class NamingService:
    def build_title(self, request: GenerateRequest, variant_index: int) -> str:
        prefix = STONE_PREFIX[request.stone]
        titles = TITLE_MAP[request.jewelleryType]
        suffix = titles[variant_index % len(titles)]
        return f"{prefix} {suffix}"
