from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes_analyze import router as analyze_router
from app.api.routes_generate import router as generate_router
from app.api.routes_health import router as health_router
from app.api.routes_query import router as query_router
from app.api.routes_upload import router as upload_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.debug)

app = FastAPI(title="Aurelium API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(generate_router)
app.include_router(query_router)

assets_root = settings.local_data_root
assets_root.mkdir(parents=True, exist_ok=True)
app.mount("/assets", StaticFiles(directory=Path(assets_root)), name="assets")

static_root = Path(__file__).parent / "static"
if static_root.exists():
    app.mount("/static", StaticFiles(directory=static_root), name="static")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str):
        if full_path.startswith("api") or full_path.startswith("assets") or full_path.startswith("health"):
            raise HTTPException(status_code=404, detail="Not found")
        target = static_root / full_path
        if full_path and target.exists() and target.is_file():
            return FileResponse(target)
        return FileResponse(static_root / "index.html")
