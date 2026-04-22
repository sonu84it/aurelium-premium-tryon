from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.schemas import AnalyzeResponse, AvailableZones, ConsultationProfile
from app.services.availability_service import AvailabilityService
from app.services.bigquery_service import BigQueryService
from app.services.consultation_service import ConsultationService
from app.services.image_validation import ImageValidationService
from app.services.landmark_service import LandmarkService
from app.services.storage_service import StorageService
from app.utils.errors import ValidationError

router = APIRouter(prefix="/api", tags=["analyze"])


class AnalyzeRequest(BaseModel):
    image_id: str
    consultationProfile: ConsultationProfile | None = None


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_portrait(payload: AnalyzeRequest) -> AnalyzeResponse:
    storage = StorageService()
    try:
        path = storage.load_upload_path(payload.image_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Portrait not found.") from exc

    try:
        validation = ImageValidationService().validate_or_raise(path)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    analysis = LandmarkService().analyze(path)
    availability, detected, warnings = AvailabilityService().evaluate(analysis)
    warnings = validation.warnings + warnings
    recommendations = [item.recommendation for item in availability.values() if item.recommendation]
    recommendations.extend(ConsultationService().build_recommendations(payload.consultationProfile))

    response = AnalyzeResponse(
        image_id=payload.image_id,
        availableZones=AvailableZones(
            nosePin=availability["nosePin"].available,
            earrings=availability["earrings"].available,
            necklace=availability["necklace"].available,
            ring=availability["ring"].available,
        ),
        qualityWarnings=warnings,
        detectedInfo=detected,
        luxuryRecommendations=recommendations,
        availability=availability,
        consultationProfile=payload.consultationProfile,
    )
    storage.save_json("metadata", f"{payload.image_id}-analysis.json", response.model_dump())
    BigQueryService().record_analysis(response.model_dump())

    return response
