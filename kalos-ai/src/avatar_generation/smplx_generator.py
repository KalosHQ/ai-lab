"""
SMPL-X mesh generation and export.

Loads SMPL-X model files from models/smplx/, runs the forward pass
with given shape parameters, and exports the resulting body mesh.
"""

import os
from pathlib import Path
from typing import Optional

import torch
import trimesh
import smplx
import numpy as np

# Path to the directory containing SMPLX_MALE.npz, SMPLX_FEMALE.npz, SMPLX_NEUTRAL.npz
MODEL_DIR = Path(os.environ.get("SMPLX_MODEL_DIR", "models/smplx"))
OUTPUT_DIR = Path(os.environ.get("SMPLX_OUTPUT_DIR", "output"))

# Gender → model file basename expected by the smplx library
GENDER_MAP = {
    "male": "male",
    "female": "female",
    "neutral": "neutral",
}


class SMPLXGenerator:
    """Manages SMPL-X model instances and generates 3D body meshes."""

    def __init__(self, model_dir: Optional[str] = None, device: str = "cpu"):
        self.device = torch.device(device)
        self.model_dir = Path(model_dir) if model_dir else MODEL_DIR
        self._models = {}  # dict[str, smplx model]

        if not self.model_dir.exists():
            raise FileNotFoundError(
                f"SMPL-X model directory not found: {self.model_dir}\n"
                "Download models from https://smpl-x.is.tue.mpg.de/ and place "
                ".npz files in models/smplx/"
            )

    def _get_model(self, gender: str, num_betas: int = 10) -> smplx.SMPLXLayer:
        """Load (and cache) a SMPL-X model for the given gender."""
        key = f"{gender}_{num_betas}"
        if key not in self._models:
            gender_label = GENDER_MAP.get(gender, "neutral")
            model = smplx.create(
                model_path=str(self.model_dir.parent),  # parent of "smplx/" folder
                model_type="smplx",
                gender=gender_label,
                num_betas=num_betas,
                use_pca=False,
                flat_hand_mean=True,
            ).to(self.device)
            model.eval()
            self._models[key] = model
        return self._models[key]

    @torch.no_grad()
    def generate_mesh(
        self,
        betas: torch.Tensor,
        gender: str = "neutral",
    ) -> trimesh.Trimesh:
        """
        Run SMPL-X forward pass and return a trimesh.Trimesh.

        Args:
            betas: Shape parameters tensor of shape (1, num_betas).
            gender: "male", "female", or "neutral".

        Returns:
            A trimesh.Trimesh with the generated body mesh.
        """
        num_betas = betas.shape[-1]
        model = self._get_model(gender, num_betas)

        output = model(betas=betas.to(self.device))
        vertices = output.vertices.squeeze(0).cpu().numpy()
        faces = model.faces.astype(np.int32)

        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
        return mesh

    def export(
        self,
        mesh: trimesh.Trimesh,
        filename: str = "avatar",
        export_format: str = "obj",
    ) -> str:
        """
        Export a trimesh to disk as .obj or .gltf.

        Args:
            mesh: The body mesh to export.
            filename: Base name (without extension) for the output file.
            export_format: "obj" or "gltf".

        Returns:
            Absolute path to the exported file.
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        fmt = export_format.lower()
        if fmt not in ("obj", "gltf"):
            raise ValueError(f"Unsupported format '{fmt}'. Use 'obj' or 'gltf'.")

        ext = "obj" if fmt == "obj" else "gltf"
        out_path = OUTPUT_DIR / f"{filename}.{ext}"

        if fmt == "obj":
            mesh.export(str(out_path), file_type="obj")
        else:
            mesh.export(str(out_path), file_type="gltf")

        return str(out_path)
