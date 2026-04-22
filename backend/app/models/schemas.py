from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class JewelleryType(str, Enum):
    earrings = "earrings"
    necklace = "necklace"
    nose_pin = "nose_pin"
    ring = "ring"


class MetalType(str, Enum):
    yellow_gold = "yellow_gold"
    white_gold = "white_gold"
    rose_gold = "rose_gold"
    platinum = "platinum"


class StoneType(str, Enum):
    diamond = "diamond"
    emerald = "emerald"
    ruby = "ruby"
    sapphire = "sapphire"


class StyleType(str, Enum):
    signature_minimal = "signature_minimal"
    evening_elegance = "evening_elegance"
    bridal_heirloom = "bridal_heirloom"
    contemporary_couture = "contemporary_couture"


class ScaleType(str, Enum):
    refined = "refined"
    statement = "statement"
    grand = "grand"


class PresentationType(str, Enum):
    feminine = "feminine"
    masculine = "masculine"
    universal = "universal"


class AgeBandType(str, Enum):
    under_30 = "under_30"
    between_30_and_50 = "between_30_and_50"
    over_50 = "over_50"


class UploadResponse(BaseModel):
    image_id: str
    original_url: str


class ZoneAvailability(BaseModel):
    available: bool
    confidence: float
    reason: Optional[str] = None
    recommendation: Optional[str] = None


class AvailableZones(BaseModel):
    nosePin: bool
    earrings: bool
    necklace: bool
    ring: bool


class DetectedInfo(BaseModel):
    faces: int = 0
    hands: int = 0
    faceAngle: str = "unknown"
    neckVisible: bool = False


class AnalyzeResponse(BaseModel):
    image_id: str
    availableZones: AvailableZones
    qualityWarnings: List[str]
    detectedInfo: DetectedInfo
    luxuryRecommendations: List[str]
    availability: Dict[str, ZoneAvailability]
    consultationProfile: Optional["ConsultationProfile"] = None


class ConsultationProfile(BaseModel):
    presentation: Optional[PresentationType] = None
    ageBand: Optional[AgeBandType] = None


class PlacementInput(BaseModel):
    side: Optional[str] = None
    finger: Optional[str] = None
    pendantLength: Optional[str] = None


class GenerateRequest(BaseModel):
    image_id: str
    jewelleryType: JewelleryType
    metal: MetalType
    stone: StoneType
    style: StyleType
    scale: ScaleType
    variant: Optional[str] = None
    placement: PlacementInput = Field(default_factory=PlacementInput)
    variants: int = Field(default=2, ge=1, le=3)


class ResultMetadata(BaseModel):
    maskPreviewUrl: Optional[str] = None
    zone: str


class GeneratedResult(BaseModel):
    url: str
    title: str
    metadata: ResultMetadata


class GenerateResponse(BaseModel):
    job_id: str
    results: List[GeneratedResult]


class HealthResponse(BaseModel):
    status: str
    configFlags: Dict[str, bool]
    providerReadiness: Dict[str, bool]


class QueryUploadsResponse(BaseModel):
    items: List[Dict]


class QueryGenerationsResponse(BaseModel):
    items: List[Dict]


class AnalyticsSummaryResponse(BaseModel):
    uploads: int
    analyses: int
    generations: int
    topJewelleryTypes: List[Dict[str, int | str]]
