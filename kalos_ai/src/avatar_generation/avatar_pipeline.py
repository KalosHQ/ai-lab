"""
Avatar generation pipeline.
Single entry point for the backend to generate a 3D avatar from user measurements.
"""

from pathlib import Path
from typing import Optional

from src.avatar_generation.body_mapper import map_to_betas
from src.avatar_generation.smplx_generator import SMPLXGenerator


def generate_avatar(
    height_cm: float,
    weight_kg: float,
    body_type: str,
    gender: str,
    model_dir: str,
    output_dir: str,
    filename: str = "avatar",
    export_format: str = "obj"
) -> str:
    """
    Full pipeline: user measurements → 3D mesh file.

    Args:
        height_cm:     User height in centimeters (e.g. 175.0)
        weight_kg:     User weight in kilograms (e.g. 70.0)
        body_type:     One of "slim", "athletic", "average", "curvy", "plus"
        gender:        One of "male", "female", "neutral"
        model_dir:     Path to the folder containing SMPL-X .npz model files
        output_dir:    Path to the folder where the mesh file will be saved
        filename:      Name of the output file without extension (e.g. "user_123")
        export_format: "obj" or "gltf"

    Returns:
        Absolute path to the exported mesh file (e.g. "/output/user_123.obj")
    
    Raises:
        FileNotFoundError: If model_dir does not exist
        ValueError: If export_format is not "obj" or "gltf"

    Example:
        >>> path = generate_avatar(
        ...     height_cm=175,
        ...     weight_kg=70,
        ...     body_type="athletic",
        ...     gender="male",
        ...     model_dir="/path/to/models/smplx",
        ...     output_dir="/path/to/output",
        ...     filename="user_123",
        ...     export_format="obj"
        ... )
        >>> print(path)  # /path/to/output/user_123.obj
    """

    # Step 1: Convert measurements to betas
    betas = map_to_betas(
        height_cm=height_cm,
        weight_kg=weight_kg,
        body_type=body_type,
        gender=gender
    )

    # Step 2: Load model and generate 3D mesh
    generator = SMPLXGenerator(model_dir=model_dir)
    mesh = generator.generate_mesh(betas=betas, gender=gender)

    # Step 3: Export mesh and return file path
    output_path = generator.export(
        mesh=mesh,
        filename=filename,
        export_format=export_format,
        output_dir=output_dir
    )

    return output_path