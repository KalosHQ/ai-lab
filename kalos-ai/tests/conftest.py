import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock heavy modules before they are imported by any application code
sys.modules["trimesh"] = MagicMock()
sys.modules["smplx"] = MagicMock()

from fastapi.testclient import TestClient

# Mock smplx_generator before it gets imported by the app
# specifically inside the lifespan of the api.main
from api.main import app

@pytest.fixture(scope="session")
def mock_generator():
    """Provides a mocked SMPLXGenerator that bypasses PyTorch operations."""
    mock = MagicMock()
    
    # When exported, just return the path we give it or a fake path
    mock.export.return_value = "dummy_path.obj"
    
    return mock

@pytest.fixture(scope="module")
def client(mock_generator):
    """
    TestClient fixture that patches the SMPLXGenerator class in main.py.
    This simulates the lifespan event successfully loading our mock.
    """
    with patch("api.main.SMPLXGenerator", return_value=mock_generator):
        with TestClient(app) as test_client:
            yield test_client
