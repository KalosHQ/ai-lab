"""
Maps user body measurements to SMPL-X shape parameters (betas).

SMPL-X betas are a 10-dimensional PCA vector controlling body shape.
This module provides a heuristic linear mapping suitable for an MVP.
A production system would train a regressor on anthropometric survey data.
"""

import torch
import numpy as np

# --- Baseline reference values (approximate population means) ---
BASELINE = {
    "male":   {"height_cm": 175.0, "weight_kg": 78.0},
    "female": {"height_cm": 163.0, "weight_kg": 65.0},
    "neutral": {"height_cm": 169.0, "weight_kg": 71.5},
}

# --- Scaling factors ---
# These control how strongly each measurement influences the corresponding beta.
# Tuned empirically to produce visually plausible shape variation.
HEIGHT_SCALE = 0.10   # beta units per cm deviation
WEIGHT_SCALE = 0.06   # beta units per kg deviation

# --- Body-type modifier presets ---
# Applied as offsets to betas[2], betas[3], betas[4].
# These encode torso width, hip ratio, and shoulder breadth respectively.
BODY_TYPE_MODIFIERS = {
    "slim":      [-1.0, -0.5, -0.3],
    "athletic":  [ 0.5,  0.8,  1.2],
    "average":   [ 0.0,  0.0,  0.0],
    "curvy":     [ 1.2,  1.5,  0.2],
    "plus":      [ 1.8,  1.0,  0.5],
}


def map_to_betas(
    height_cm: float,
    weight_kg: float,
    body_type: str = "average",
    gender: str = "neutral",
    num_betas: int = 10,
) -> torch.Tensor:
    """
    Convert user-provided body descriptors to a SMPL-X beta vector.

    Args:
        height_cm: User height in centimeters.
        weight_kg: User weight in kilograms.
        body_type: One of "slim", "athletic", "average", "curvy", "plus".
        gender: One of "male", "female", "neutral".
        num_betas: Number of shape coefficients (default 10).

    Returns:
        A (1, num_betas) float32 tensor suitable for smplx forward pass.
    """
    betas = np.zeros(num_betas, dtype=np.float32)

    # Look up baseline for this gender (fall back to neutral)
    ref = BASELINE.get(gender, BASELINE["neutral"])

    # Beta[0]: body mass / volume
    betas[0] = (weight_kg - ref["weight_kg"]) * WEIGHT_SCALE

    # Beta[1]: height
    betas[1] = (height_cm - ref["height_cm"]) * HEIGHT_SCALE

    # Beta[2:5]: body-type modifiers
    body_type = body_type.lower()
    modifiers = BODY_TYPE_MODIFIERS.get(body_type, BODY_TYPE_MODIFIERS["average"])
    for i, val in enumerate(modifiers):
        betas[2 + i] = val

    return torch.tensor(betas, dtype=torch.float32).unsqueeze(0)  # shape (1, num_betas)
