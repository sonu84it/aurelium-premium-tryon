from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Aurelium"
    debug: bool = False
    api_prefix: str = "/api"
    allowed_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    google_cloud_project: str = ""
    google_cloud_location: str = ""
    gcs_bucket_name: str = ""
    gcs_public_base_url: str = ""
    vertex_imagen_edit_model: str = ""
    bq_dataset_id: str = "aurelium"
    bq_table_uploads: str = "uploads"
    bq_table_analysis: str = "analysis"
    bq_table_generations: str = "generations"

    storage_mode: str = "local"
    local_data_root: Path = Path("data")

    min_image_width: int = 768
    min_image_height: int = 768
    min_recoverable_width: int = 480
    min_recoverable_height: int = 480
    min_face_ratio: float = 0.16
    max_blur_variance: float = 75.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        enable_decoding=False,
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.local_data_root.mkdir(parents=True, exist_ok=True)
    return settings
