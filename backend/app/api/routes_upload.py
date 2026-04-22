from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import UploadResponse
from app.services.bigquery_service import BigQueryService
from app.services.image_validation import ImageValidationService
from app.services.storage_service import StorageService
from app.utils.errors import ValidationError

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_image(image: UploadFile = File(...)) -> UploadResponse:
    storage = StorageService()
    image_id = storage.create_image_id()
    stored = storage.save_upload(image_id=image_id, file_name=image.filename or "portrait.png", file_obj=image.file)

    try:
        ImageValidationService().validate_or_raise(stored.path)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    BigQueryService().record_upload(image_id=image_id, original_url=stored.url, file_name=image.filename or "portrait.png")

    return UploadResponse(image_id=image_id, original_url=stored.url)
