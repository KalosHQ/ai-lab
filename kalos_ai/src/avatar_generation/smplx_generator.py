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

def _create_a_pose():
    """Create A-pose parameters (arms down at ~20 degrees)."""
    pose = np.zeros(63, dtype=np.float32)
    # Shoulder joints are at indices 6-8 (left) and 9-11 (right)
    # Rotate shoulders downward (positive X rotation)
    pose[6:9] = [0.35, 0.0, 0.0]   # Left shoulder: 20° down
    pose[9:12] = [0.35, 0.0, 0.0]  # Right shoulder: 20° down
    return pose

def _create_natural_pose():
    """Create natural standing pose (slight elbow bend)."""
    pose = np.zeros(63, dtype=np.float32)
    # Shoulders down
    pose[6:9] = [0.4, 0.0, 0.0]    # Left shoulder
    pose[9:12] = [0.4, 0.0, 0.0]   # Right shoulder
    # Slight elbow bend
    pose[12:15] = [0.1, 0.0, 0.0]  # Left elbow
    pose[15:18] = [0.1, 0.0, 0.0]  # Right elbow
    return pose

# SMPL-X pose presets (defined after helper functions)
POSE_PRESETS = {
    "t-pose": np.zeros(63, dtype=np.float32),  # Default T-pose
    "a-pose": _create_a_pose(),
    "natural": _create_natural_pose(),
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
        pose: str = "a-pose",
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

        body_pose = POSE_PRESETS.get(pose, POSE_PRESETS["a-pose"])
        body_pose_tensor = torch.tensor(
            body_pose, dtype=torch.float32, device=self.device).unsqueeze(0)

        output = model(
            betas=betas.to(self.device),
            body_pose=body_pose_tensor
        )
        vertices = output.vertices.squeeze(0).cpu().numpy()
        faces = model.faces.astype(np.int32)

        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
        return mesh

    def export(
        self,
        mesh: trimesh.Trimesh,
        filename: str = "avatar",
        export_format: str = "obj",
        output_dir: Optional[str] = None,
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
        out_dir = Path(output_dir) if output_dir else OUTPUT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)

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
