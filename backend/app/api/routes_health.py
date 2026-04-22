from fastapi import APIRouter

from app.core.config import get_settings
from app.models.schemas import HealthResponse
from app.services.bigquery_service import BigQueryService
from app.services.imagen_service import ImagenService

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    imagen = ImagenService()
    bigquery_service = BigQueryService()
    return HealthResponse(
        status="ok",
        configFlags={
            "debug": settings.debug,
            "storageLocal": settings.storage_mode == "local",
        },
        providerReadiness={
            **imagen.provider_status(),
            "bigQueryConfigured": bigquery_service.is_ready(),
        },
    )
