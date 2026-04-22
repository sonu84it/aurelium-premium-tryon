from fastapi import APIRouter, Query

from app.models.schemas import AnalyticsSummaryResponse, QueryGenerationsResponse, QueryUploadsResponse
from app.services.bigquery_service import BigQueryService

router = APIRouter(prefix="/api/query", tags=["query"])


@router.get("/uploads", response_model=QueryUploadsResponse)
def query_uploads(limit: int = Query(default=20, ge=1, le=100)) -> QueryUploadsResponse:
    items = BigQueryService().list_uploads(limit=limit)
    return QueryUploadsResponse(items=items)


@router.get("/generations", response_model=QueryGenerationsResponse)
def query_generations(image_id: str | None = None, limit: int = Query(default=20, ge=1, le=100)) -> QueryGenerationsResponse:
    items = BigQueryService().list_generations(image_id=image_id, limit=limit)
    return QueryGenerationsResponse(items=items)


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
def analytics_summary() -> AnalyticsSummaryResponse:
    return AnalyticsSummaryResponse(**BigQueryService().analytics_summary())
