"""
Avatar generation route.

POST /api/ai/generate-avatar
"""

import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from schemas import AvatarRequest, AvatarResponse
from avatar.body_mapper import map_to_betas

router = APIRouter(prefix="/api/ai", tags=["avatar"])


@router.post("/generate-avatar", response_model=AvatarResponse)
async def generate_avatar(req: AvatarRequest):
    """Generate a 3D body mesh from user measurements."""
    # Import here to access the shared instance set during lifespan
    from api.main import generator

    if generator is None:
        raise HTTPException(
            status_code=503,
            detail="SMPL-X models are not loaded. Place model files in models/smplx/ and restart.",
        )

    # 1. Map inputs → SMPL-X betas
    betas = map_to_betas(
        height_cm=req.height_cm,
        weight_kg=req.weight_kg,
        body_type=req.body_type.value,
        gender=req.gender.value,
    )

    # 2. Generate mesh
    mesh = generator.generate_mesh(betas=betas, gender=req.gender.value)

    # 3. Export to file
    filename = f"avatar_{uuid.uuid4().hex[:8]}"
    out_path = generator.export(mesh, filename=filename, export_format=req.export_format.value)

    # 4. Return the file as a download
    media_type = "model/obj" if req.export_format.value == "obj" else "model/gltf+json"
    ext = req.export_format.value

    return FileResponse(
        path=out_path,
        filename=f"{filename}.{ext}",
        media_type=media_type,
    )
