from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from src.powerplant_challenge.main import app


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as client:
        yield client
        app.dependency_overrides = {}
