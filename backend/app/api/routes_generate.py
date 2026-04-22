from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException
from PIL import Image

from app.models.schemas import GenerateRequest, GenerateResponse, GeneratedResult, ResultMetadata
from app.services.imagen_service import ImagenService
from app.services.landmark_service import LandmarkService
from app.services.luxury_prompt_builder import LuxuryPromptBuilder
from app.services.mask_service import MaskService
from app.services.naming_service import NamingService
from app.services.bigquery_service import BigQueryService
from app.services.storage_service import StorageService
from app.utils.errors import ProviderUnavailableError

router = APIRouter(prefix="/api", tags=["generate"])


@router.post("/generate", response_model=GenerateResponse)
def generate_preview(payload: GenerateRequest) -> GenerateResponse:
    storage = StorageService()
    try:
        upload_path = storage.load_upload_path(payload.image_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Portrait not found.") from exc

    analysis = LandmarkService().analyze(upload_path)
    mask_image, _boxes = MaskService().build_mask(payload, analysis)
    mask_stored = storage.save_image("masks", f"{payload.image_id}-{payload.jewelleryType.value}", mask_image)

    prompt = LuxuryPromptBuilder().build(payload)
    try:
        results = ImagenService().generate(upload_path, mask_image, prompt, payload, analysis)
    except ProviderUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    naming = NamingService()
    job_id = uuid.uuid4().hex

    generated_results = []
    for index, result in enumerate(results):
        stored = storage.save_image("results", f"{job_id}-{index}", result.image, suffix=".jpg")
        generated_results.append(
            GeneratedResult(
                url=stored.url,
                title=naming.build_title(payload, index),
                metadata=ResultMetadata(maskPreviewUrl=mask_stored.url, zone=payload.jewelleryType.value),
            )
        )

    storage.save_json(
        "metadata",
        f"{job_id}.json",
        {
            "job_id": job_id,
            "request": payload.model_dump(),
            "prompt": prompt,
            "results": [item.model_dump() for item in generated_results],
        },
    )
    BigQueryService().record_generation(job_id, payload.model_dump(mode="json"), [item.model_dump() for item in generated_results])
    return GenerateResponse(job_id=job_id, results=generated_results)
