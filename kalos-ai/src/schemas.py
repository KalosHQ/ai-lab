from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


# ── Avatar schemas ──────────────────────────────────────────────

class BodyType(str, Enum):
    slim = "slim"
    athletic = "athletic"
    average = "average"
    curvy = "curvy"
    plus = "plus"


class Gender(str, Enum):
    male = "male"
    female = "female"
    neutral = "neutral"


class ExportFormat(str, Enum):
    obj = "obj"
    gltf = "gltf"


class AvatarRequest(BaseModel):
    height_cm: float = Field(..., gt=100, lt=250, description="Height in centimeters")
    weight_kg: float = Field(..., gt=30, lt=300, description="Weight in kilograms")
    body_type: BodyType = Field(default=BodyType.average, description="Body type preset")
    gender: Gender = Field(default=Gender.neutral, description="Gender for model selection")
    export_format: ExportFormat = Field(default=ExportFormat.obj, description="3D file format")


class AvatarResponse(BaseModel):
    filename: str = Field(..., description="Name of the generated file")
    format: str = Field(..., description="Export format used")
    vertices: int = Field(..., description="Number of vertices in the mesh")
    faces: int = Field(..., description="Number of faces in the mesh")


# ── Clothing detection schemas ──────────────────────────────────

class ClothingAttributes(BaseModel):
    color: Optional[str] = Field(None, description="Dominant color of the clothing item")
    pattern: Optional[str] = Field(None, description="Pattern of the clothing item (e.g., solid, floral, striped)")
    material: Optional[str] = Field(None, description="Perceived material (e.g., denim, cotton, leather)")

class ClothingItem(BaseModel):
    category: str = Field(..., description="Category of the clothing item (e.g., Top, Bottom, Shoes)")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    attributes: Optional[ClothingAttributes] = Field(None, description="Detailed attributes of the item")
    box_2d: Optional[List[int]] = Field(None, description="Bounding box [ymin, xmin, ymax, xmax] if detectable. 0-1000 scale preferred by Gemini.")

class DetectionResponse(BaseModel):
    items: List[ClothingItem] = Field(default_factory=list, description="List of detected clothing items")
