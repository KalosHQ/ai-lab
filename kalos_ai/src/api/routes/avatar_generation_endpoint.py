"""
Avatar generation route.

POST /api/ai/generate-avatar
"""

import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from src.avatar_generation.schema import AvatarRequest, AvatarResponse
from src.avatar_generation.avatar_pipeline import generate_avatar as generate_avatar_pipeline

router = APIRouter(prefix="/api/ai", tags=["avatar"])


@router.post("/generate-avatar", response_model=AvatarResponse)
async def generate_avatar(req: AvatarRequest):
    """Generate a 3D body mesh from user measurements."""
    # Use the unified avatar pipeline
    filename = f"avatar_{uuid.uuid4().hex[:8]}"
    
    try:
        # Call the pipeline function
        out_path = generate_avatar_pipeline(
            height_cm=req.height_cm,
            weight_kg=req.weight_kg,
            body_type=req.body_type.value,
            gender=req.gender.value,
            model_dir="models/smplx",
            output_dir="output",
            filename=filename,
            export_format=req.export_format.value
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail=f"SMPL-X models not found. Place model files in models/smplx/ and restart. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating avatar: {str(e)}"
        )

    # Return the file as a download
    media_type = "model/obj" if req.export_format.value == "obj" else "model/gltf+json"
    ext = req.export_format.value

    return FileResponse(
        path=out_path,
        filename=f"{filename}.{ext}",
        media_type=media_type,
    )
