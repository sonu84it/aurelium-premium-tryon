# Aurelium

Aurelium is a luxury no-prompt AI jewellery virtual try-on MVP for premium brands and high-value customers. Users upload a portrait, receive consultation-style suitability feedback, choose from curated premium jewellery selections, and generate refined preview variants without typing prompts.

## Stack

- Frontend: React, Vite, TypeScript, Tailwind CSS, React Query, Zustand, react-dropzone, react-compare-slider
- Backend: FastAPI, Python 3.11, Pillow, NumPy, OpenCV, MediaPipe-ready analysis services
- Cloud targets: Google Cloud Storage, Vertex AI Imagen editing, Cloud Run, Vercel or Netlify

## File Tree

```text
backend/
  app/
    api/
    core/
    models/
    services/
    utils/
    main.py
  tests/
  Dockerfile
  requirements.txt
frontend/
  src/
    app/
    components/
    hooks/
    lib/
    pages/
    services/
    styles/
    types/
    main.tsx
  components.json
  index.html
  package.json
  tailwind.config.ts
README.md
```

## Setup

### Backend

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Copy these into `backend/.env`:

```env
GOOGLE_CLOUD_PROJECT=
GOOGLE_CLOUD_LOCATION=
GCS_BUCKET_NAME=
GCS_PUBLIC_BASE_URL=
VERTEX_IMAGEN_EDIT_MODEL=
BQ_DATASET_ID=aurelium
DEBUG=false
ALLOWED_ORIGINS=http://localhost:5173
STORAGE_MODE=local
LOCAL_DATA_ROOT=data
```

Optionally set `VITE_API_BASE_URL=http://localhost:8000` in `frontend/.env`.

## API Flow

1. `POST /api/upload`
   Uploads the portrait and validates resolution and blur suitability.
2. `POST /api/analyze`
   Runs deterministic analysis, returning available try-on zones, warnings, and luxury recommendations.
3. `POST /api/generate`
   Builds a precise mask, translates structured selections into hidden premium edit instructions, and returns 2-3 preview variants.
4. `GET /api/query/uploads`
   Returns recent uploaded portraits from BigQuery.
5. `GET /api/query/generations`
   Returns recent generation jobs, optionally filtered by `image_id`.
6. `GET /api/query/analytics/summary`
   Returns upload, analysis, and generation totals plus top jewellery categories.

## Landmark and Mask Architecture

- `landmark_service.py`
  Produces deterministic portrait anchors for ears, nostril, neck, chest, and ring fingers. MediaPipe is prepared as the analysis provider, with a conservative fallback strategy for local development.
- `availability_service.py`
  Converts landmark visibility into confidence-scored jewellery availability with luxury consultation copy.
- `mask_service.py`
  Generates binary masks for earrings, necklace, nose pin, and ring zones, then feathers edges for realistic editing handoff.

## Prompt Generation Approach

- Users never type prompts.
- `luxury_prompt_builder.py` converts structured premium selections into hidden edit instructions.
- Prompts preserve identity, skin tone, hair, clothing, proportions, and background while restricting edits to the jewellery region only.

## Provider Strategy

- `VertexImagenEditor` is env-driven and checks readiness from:
  - `GOOGLE_CLOUD_PROJECT`
  - `GOOGLE_CLOUD_LOCATION`
  - `VERTEX_IMAGEN_EDIT_MODEL`
- A local fallback preview renderer keeps the MVP demoable even before production Vertex credentials are wired.

## BigQuery

- `bigquery_service.py` persists upload, analysis, and generation metadata into BigQuery.
- Dataset and tables are created lazily on first use when Google Cloud configuration is available.
- Query endpoints allow the app or internal tools to read recent uploads, generations, and summary analytics.

## Cloud Deployment Notes

- Use `STORAGE_MODE=gcs` on Cloud Run so uploads, masks, results, and metadata persist outside the container filesystem.
- Set `GCS_BUCKET_NAME` and `GCS_PUBLIC_BASE_URL=https://storage.googleapis.com/<bucket-name>`.
- The frontend can also be containerized and deployed to Cloud Run with `VITE_API_BASE_URL` pointing at the backend service URL.

## Debug and Storage Layout

Generated assets are stored under:

- `uploads/`
- `masks/`
- `debug/`
- `results/`
- `metadata/`

These are served locally from `/assets/*` in development.

## Tests

Run the backend unit tests:

```bash
cd backend
pytest
```

Included tests cover:

- luxury prompt builder
- availability logic
- mask utilities
- naming service

## Known Limitations

- MediaPipe landmarks currently fall back to a conservative heuristic strategy for local MVP continuity.
- Vertex Imagen runtime editing is prepared as an abstraction but still needs credentialed project integration before production deployment.
- The fallback preview renderer is for demo continuity and not a substitute for true inpainting quality.

## Roadmap

- Full MediaPipe Tasks integration for face, hand, and pose models
- GCS-backed asset persistence and signed delivery URLs
- Production Vertex Imagen editing flow with retries and structured safety handling
- Higher-resolution exports and premium result collections
- Luxury brand theming packs and collection-specific preset curation
