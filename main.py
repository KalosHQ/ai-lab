"""
Kalos AI — FastAPI application entry point.

Run with:
    uvicorn main:app --reload --port 8000
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the parent of src to the import path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'kalos_ai'))

from kalos_ai.src.avatar_generation.smplx_generator import SMPLXGenerator
from kalos_ai.src.api.routes.avatar_generation_endpoint import router as avatar_router
from kalos_ai.src.utils.download_models import download_models

# Shared generator instance — populated at startup
generator: Optional[SMPLXGenerator] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load SMPL-X models into memory on startup."""
    global generator
    try:
        download_models()
        generator = SMPLXGenerator()
        # Warm the cache for all three genders
        for g in ("neutral", "male", "female"):
            generator._get_model(g)
        print("✅ SMPL-X models loaded successfully.")
    except FileNotFoundError as e:
        print(f"⚠️  SMPL-X models not found — avatar endpoint will return 503.\n{e}")
        generator = None
    yield
    # Cleanup (nothing to do for now)


app = FastAPI(
    title="Kalos AI",
    description="Fashion-tech API: 3D avatar generation and clothing detection.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(avatar_router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "smplx_loaded": generator is not None,
    }