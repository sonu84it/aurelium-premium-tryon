from __future__ import annotations

import json
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
import tempfile
from typing import Any, BinaryIO

from PIL import Image

from app.core.config import get_settings

try:
    from google.cloud import storage
except ImportError:  # pragma: no cover
    storage = None


@dataclass
class StoredObject:
    path: Path
    url: str


class StorageService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.root = self.settings.local_data_root
        self.storage_mode = self.settings.storage_mode.lower()
        self.bucket_name = self.settings.gcs_bucket_name
        self.gcs_base_url = self.settings.gcs_public_base_url or (
            f"https://storage.googleapis.com/{self.bucket_name}" if self.bucket_name else ""
        )
        self._gcs_client = None
        if self.storage_mode == "local":
            for folder in ["uploads", "masks", "debug", "results", "metadata"]:
                (self.root / folder).mkdir(parents=True, exist_ok=True)

    def create_image_id(self) -> str:
        return uuid.uuid4().hex

    def save_upload(self, image_id: str, file_name: str, file_obj: BinaryIO) -> StoredObject:
        suffix = Path(file_name).suffix or ".png"
        object_name = f"uploads/{image_id}{suffix}"
        if self.storage_mode == "gcs":
            path = Path(tempfile.gettempdir()) / f"{image_id}{suffix}"
            with path.open("wb") as output:
                shutil.copyfileobj(file_obj, output)
            self._upload_file(path, object_name)
            return StoredObject(path=path, url=self._gcs_url(object_name))

        path = self.root / object_name
        with path.open("wb") as output:
            shutil.copyfileobj(file_obj, output)
        return StoredObject(path=path, url=self._local_url(path))

    def load_upload_path(self, image_id: str) -> Path:
        if self.storage_mode == "gcs":
            bucket = self._bucket()
            blobs = list(bucket.list_blobs(prefix=f"uploads/{image_id}."))
            if not blobs:
                raise FileNotFoundError(f"Upload not found for image_id={image_id}")
            suffix = Path(blobs[0].name).suffix or ".png"
            path = Path(tempfile.gettempdir()) / f"{image_id}{suffix}"
            blobs[0].download_to_filename(path)
            return path

        matches = list((self.root / "uploads").glob(f"{image_id}.*"))
        if not matches:
            raise FileNotFoundError(f"Upload not found for image_id={image_id}")
        return matches[0]

    def save_image(self, category: str, image_id: str, image: Image.Image, suffix: str = ".png") -> StoredObject:
        object_name = f"{category}/{image_id}{suffix}"
        if self.storage_mode == "gcs":
            path = Path(tempfile.gettempdir()) / f"{image_id}{suffix}"
            image.save(path)
            self._upload_file(path, object_name)
            return StoredObject(path=path, url=self._gcs_url(object_name))

        path = self.root / object_name
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
        return StoredObject(path=path, url=self._local_url(path))

    def save_json(self, category: str, file_name: str, payload: Any) -> StoredObject:
        object_name = f"{category}/{file_name}"
        if self.storage_mode == "gcs":
            path = Path(tempfile.gettempdir()) / file_name
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            self._upload_file(path, object_name, content_type="application/json")
            return StoredObject(path=path, url=self._gcs_url(object_name))

        path = self.root / object_name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return StoredObject(path=path, url=self._local_url(path))

    def _local_url(self, path: Path) -> str:
        return f"/assets/{path.relative_to(self.root).as_posix()}"

    def _gcs_url(self, object_name: str) -> str:
        return f"{self.gcs_base_url}/{object_name}"

    def _client(self):
        if self._gcs_client is None:
            if storage is None:
                raise RuntimeError("google-cloud-storage is not installed")
            self._gcs_client = storage.Client(project=self.settings.google_cloud_project or None)
        return self._gcs_client

    def _bucket(self):
        if not self.bucket_name:
            raise RuntimeError("GCS_BUCKET_NAME is required for gcs storage mode")
        return self._client().bucket(self.bucket_name)

    def _upload_file(self, path: Path, object_name: str, content_type: str | None = None) -> None:
        blob = self._bucket().blob(object_name)
        blob.upload_from_filename(path, content_type=content_type)
