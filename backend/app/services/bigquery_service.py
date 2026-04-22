from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.core.config import get_settings

logger = logging.getLogger(__name__)

try:
    from google.cloud import bigquery
except ImportError:  # pragma: no cover
    bigquery = None


class BigQueryService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.project_id = self.settings.google_cloud_project
        self.dataset_id = self.settings.bq_dataset_id
        self._client = None

    def is_ready(self) -> bool:
        return bool(self.project_id and bigquery is not None)

    def _client_or_none(self):
        if not self.is_ready():
            return None
        if self._client is None:
            self._client = bigquery.Client(project=self.project_id)
        return self._client

    def ensure_schema(self) -> bool:
        client = self._client_or_none()
        if client is None:
            return False

        dataset_ref = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
        dataset_ref.location = self.settings.google_cloud_location or "us-central1"
        client.create_dataset(dataset_ref, exists_ok=True)

        self._ensure_table(
            self.settings.bq_table_uploads,
            [
                bigquery.SchemaField("image_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("original_url", "STRING"),
                bigquery.SchemaField("file_name", "STRING"),
                bigquery.SchemaField("created_at", "TIMESTAMP"),
            ],
        )
        self._ensure_table(
            self.settings.bq_table_analysis,
            [
                bigquery.SchemaField("image_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("faces", "INTEGER"),
                bigquery.SchemaField("hands", "INTEGER"),
                bigquery.SchemaField("face_angle", "STRING"),
                bigquery.SchemaField("neck_visible", "BOOLEAN"),
                bigquery.SchemaField("quality_warnings", "STRING", mode="REPEATED"),
                bigquery.SchemaField("recommendations", "STRING", mode="REPEATED"),
                bigquery.SchemaField("created_at", "TIMESTAMP"),
            ],
        )
        self._ensure_table(
            self.settings.bq_table_generations,
            [
                bigquery.SchemaField("job_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("image_id", "STRING"),
                bigquery.SchemaField("jewellery_type", "STRING"),
                bigquery.SchemaField("metal", "STRING"),
                bigquery.SchemaField("stone", "STRING"),
                bigquery.SchemaField("style", "STRING"),
                bigquery.SchemaField("scale", "STRING"),
                bigquery.SchemaField("variant", "STRING"),
                bigquery.SchemaField("result_titles", "STRING", mode="REPEATED"),
                bigquery.SchemaField("result_urls", "STRING", mode="REPEATED"),
                bigquery.SchemaField("created_at", "TIMESTAMP"),
            ],
        )
        return True

    def _ensure_table(self, table_name: str, schema: list) -> None:
        client = self._client_or_none()
        if client is None:
            return
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        table = bigquery.Table(table_id, schema=schema)
        client.create_table(table, exists_ok=True)

    def record_upload(self, image_id: str, original_url: str, file_name: str) -> None:
        self._insert_rows(
            self.settings.bq_table_uploads,
            [{
                "image_id": image_id,
                "original_url": original_url,
                "file_name": file_name,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }],
        )

    def record_analysis(self, payload: Dict[str, Any]) -> None:
        row = {
            "image_id": payload["image_id"],
            "faces": payload["detectedInfo"]["faces"],
            "hands": payload["detectedInfo"]["hands"],
            "face_angle": payload["detectedInfo"]["faceAngle"],
            "neck_visible": payload["detectedInfo"]["neckVisible"],
            "quality_warnings": payload["qualityWarnings"],
            "recommendations": payload["luxuryRecommendations"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._insert_rows(self.settings.bq_table_analysis, [row])

    def record_generation(self, job_id: str, payload: Dict[str, Any], results: List[Dict[str, Any]]) -> None:
        row = {
            "job_id": job_id,
            "image_id": payload["image_id"],
            "jewellery_type": payload["jewelleryType"],
            "metal": payload["metal"],
            "stone": payload["stone"],
            "style": payload["style"],
            "scale": payload["scale"],
            "variant": payload.get("variant"),
            "result_titles": [item["title"] for item in results],
            "result_urls": [item["url"] for item in results],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._insert_rows(self.settings.bq_table_generations, [row])

    def list_uploads(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self._run_query(
            f"""
            SELECT image_id, original_url, file_name, created_at
            FROM `{self.project_id}.{self.dataset_id}.{self.settings.bq_table_uploads}`
            ORDER BY created_at DESC
            LIMIT @limit
            """,
            [bigquery.ScalarQueryParameter("limit", "INT64", limit)],
        )

    def list_generations(self, image_id: str | None = None, limit: int = 20) -> List[Dict[str, Any]]:
        where_clause = "WHERE image_id = @image_id" if image_id else ""
        params = [bigquery.ScalarQueryParameter("limit", "INT64", limit)]
        if image_id:
            params.append(bigquery.ScalarQueryParameter("image_id", "STRING", image_id))
        return self._run_query(
            f"""
            SELECT job_id, image_id, jewellery_type, metal, stone, style, scale, variant, result_titles, result_urls, created_at
            FROM `{self.project_id}.{self.dataset_id}.{self.settings.bq_table_generations}`
            {where_clause}
            ORDER BY created_at DESC
            LIMIT @limit
            """,
            params,
        )

    def analytics_summary(self) -> Dict[str, Any]:
        uploads = self._run_query(
            f"SELECT COUNT(*) AS total FROM `{self.project_id}.{self.dataset_id}.{self.settings.bq_table_uploads}`",
            [],
        )
        analyses = self._run_query(
            f"SELECT COUNT(*) AS total FROM `{self.project_id}.{self.dataset_id}.{self.settings.bq_table_analysis}`",
            [],
        )
        generations = self._run_query(
            f"SELECT COUNT(*) AS total FROM `{self.project_id}.{self.dataset_id}.{self.settings.bq_table_generations}`",
            [],
        )
        top_types = self._run_query(
            f"""
            SELECT jewellery_type, COUNT(*) AS total
            FROM `{self.project_id}.{self.dataset_id}.{self.settings.bq_table_generations}`
            GROUP BY jewellery_type
            ORDER BY total DESC
            LIMIT 5
            """,
            [],
        )
        return {
            "uploads": uploads[0]["total"] if uploads else 0,
            "analyses": analyses[0]["total"] if analyses else 0,
            "generations": generations[0]["total"] if generations else 0,
            "topJewelleryTypes": top_types,
        }

    def _insert_rows(self, table_name: str, rows: List[Dict[str, Any]]) -> None:
        client = self._client_or_none()
        if client is None:
            return
        self.ensure_schema()
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        errors = client.insert_rows_json(table_id, rows)
        if errors:
            logger.warning("BigQuery insert failed for %s: %s", table_name, errors)

    def _run_query(self, query: str, query_parameters: list) -> List[Dict[str, Any]]:
        client = self._client_or_none()
        if client is None:
            return []
        self.ensure_schema()
        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        rows = client.query(query, job_config=job_config).result()
        return [dict(row.items()) for row in rows]
