import torch
import pytest

from avatar.body_mapper import map_to_betas, BASELINE, HEIGHT_SCALE, WEIGHT_SCALE

def test_map_to_betas_default():
    """Test default generation outputs a valid zero-padded tensor."""
    betas = map_to_betas(
        height_cm=BASELINE["neutral"]["height_cm"],
        weight_kg=BASELINE["neutral"]["weight_kg"],
        body_type="average",
        gender="neutral"
    )
    
    assert isinstance(betas, torch.Tensor)
    assert betas.dtype == torch.float32
    assert betas.shape == (1, 10)
    
    # With exact baseline and average type, offsets should be 0
    assert torch.all(betas == 0.0)

def test_map_to_betas_scaling_factors():
    """Test height and weight deviation maths."""
    # 10kg heavier, 10cm taller
    weight_diff = 10.0
    height_diff = 10.0
    
    betas = map_to_betas(
        height_cm=BASELINE["male"]["height_cm"] + height_diff,
        weight_kg=BASELINE["male"]["weight_kg"] + weight_diff,
        body_type="average",
        gender="male"
    )
    
    # Beta[0] is mass
    assert pytest.approx(betas[0, 0].item()) == weight_diff * WEIGHT_SCALE
    
    # Beta[1] is height
    assert pytest.approx(betas[0, 1].item()) == height_diff * HEIGHT_SCALE

def test_map_to_betas_body_type():
    """Test body modifiers applied correctly."""
    betas = map_to_betas(
        height_cm=BASELINE["female"]["height_cm"],
        weight_kg=BASELINE["female"]["weight_kg"],
        body_type="curvy",
        gender="female"
    )
    
    # Curvy modifiers: [ 1.2,  1.5,  0.2]
    assert pytest.approx(betas[0, 2].item()) == 1.2
    assert pytest.approx(betas[0, 3].item()) == 1.5
    assert pytest.approx(betas[0, 4].item()) == 0.2
    
def test_map_to_betas_custom_beta_count():
    """Test passing custom num_betas."""
    betas = map_to_betas(180, 80, num_betas=20)
    assert betas.shape == (1, 20)
