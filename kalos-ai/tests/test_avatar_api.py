import pytest

def test_generate_avatar_success(client, mock_generator, tmp_path):
    """Test a successful avatar generation, simulating the file export properly."""
    # Create a dummy file that the API will try to return
    dummy_file = tmp_path / "dummy_avatar.obj"
    dummy_file.write_text("dummy 3d object content")
    
    # Tell our mocked generator's export to return this real temporary path
    # so FastAPI can successfully read it for the FileResponse.
    mock_generator.export.return_value = str(dummy_file)
    
    req_payload = {
        "height_cm": 175.5,
        "weight_kg": 72.0,
        "body_type": "slim",
        "gender": "male",
        "export_format": "obj"
    }

    # Execute the request
    response = client.post("/api/ai/generate-avatar", json=req_payload)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "model/obj"
    # Ensure it returns the dummy content
    assert response.text == "dummy 3d object content"
    
    # Check that our mock logic was called
    mock_generator.generate_mesh.assert_called_once()
    mock_generator.export.assert_called_once()
    
    # Validate the export format matches requested
    kwargs = mock_generator.export.call_args.kwargs
    assert kwargs.get("export_format") == "obj"

def test_generate_avatar_validation_error(client):
    """Test 422 Unprocessable Entity for invalid parameters."""
    req_payload = {
        "height_cm": 10, # too small, schema demands gt=100
        "weight_kg": 72.0,
        "body_type": "invalid_type",
        "gender": "male"
    }
    
    response = client.post("/api/ai/generate-avatar", json=req_payload)
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.parametrize("format_val,expected_content_type", [
    ("obj", "model/obj"),
    ("gltf", "model/gltf+json")
])
def test_generate_avatar_formats(client, mock_generator, tmp_path, format_val, expected_content_type):
    """Test returning both obj and gltf formats."""
    dummy_file = tmp_path / f"dummy.{format_val}"
    dummy_file.write_text("content")
    mock_generator.export.return_value = str(dummy_file)
    
    req_payload = {
        "height_cm": 160.0,
        "weight_kg": 55.0,
        "export_format": format_val
    }
    
    response = client.post("/api/ai/generate-avatar", json=req_payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == expected_content_type
