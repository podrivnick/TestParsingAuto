import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.infrastructure.di.main import init_container
from src.presentation.api.main import init_api
from src.tests.unit.fixtures import init_dummy_container


@pytest.fixture
def app() -> FastAPI:
    app = init_api()
    app.dependency_overrides[init_container] = init_dummy_container

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
