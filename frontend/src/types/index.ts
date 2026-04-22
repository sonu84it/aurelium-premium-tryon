export type JewelleryType = "earrings" | "necklace" | "nose_pin" | "ring";
export type MetalType = "yellow_gold" | "white_gold" | "rose_gold" | "platinum";
export type StoneType = "diamond" | "emerald" | "ruby" | "sapphire";
export type StyleType =
  | "signature_minimal"
  | "evening_elegance"
  | "bridal_heirloom"
  | "contemporary_couture";
export type ScaleType = "refined" | "statement" | "grand";
export type PresentationType = "feminine" | "masculine" | "universal";
export type AgeBandType = "under_30" | "between_30_and_50" | "over_50";

export interface ConsultationProfile {
  presentation?: PresentationType;
  ageBand?: AgeBandType;
}

export interface UploadResponse {
  image_id: string;
  original_url: string;
}

export interface AnalyzeResponse {
  image_id: string;
  availableZones: {
    nosePin: boolean;
    earrings: boolean;
    necklace: boolean;
    ring: boolean;
  };
  qualityWarnings: string[];
  luxuryRecommendations: string[];
  detectedInfo: {
    faces: number;
    hands: number;
    faceAngle: string;
    neckVisible: boolean;
  };
  availability: Record<
    string,
    {
      available: boolean;
      confidence: number;
      reason?: string;
      recommendation?: string;
    }
  >;
  consultationProfile?: ConsultationProfile;
}

export interface GenerateRequest {
  image_id: string;
  jewelleryType: JewelleryType;
  metal: MetalType;
  stone: StoneType;
  style: StyleType;
  scale: ScaleType;
  variant?: string;
  placement: {
    side?: string;
    finger?: string;
    pendantLength?: string;
  };
  variants: number;
}

export interface GenerateResponse {
  job_id: string;
  results: Array<{
    url: string;
    title: string;
    metadata: {
      maskPreviewUrl?: string;
      zone: string;
    };
  }>;
}
