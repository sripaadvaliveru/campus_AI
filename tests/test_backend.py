"""
test_backend.py — Tests for backend/main.py FastAPI endpoints.
"""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app."""
    from backend.main import app
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for GET /health"""

    def test_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_has_required_fields(self, client):
        data = client.get("/health").json()
        assert "status" in data
        assert "api_key_set" in data
        assert "vector_store_ready" in data
        assert "provider" in data
        assert "model" in data
        assert "timestamp" in data

    def test_status_ok_when_api_key_set(self, client):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-real-key-123"}):
            data = client.get("/health").json()
            assert data["status"] == "ok"
            assert data["api_key_set"] is True

    def test_status_degraded_when_no_key(self, client):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "", "GOOGLE_API_KEY": ""}, clear=False):
            data = client.get("/health").json()
            assert data["status"] == "degraded"
            assert data["api_key_set"] is False

    def test_provider_is_string(self, client):
        data = client.get("/health").json()
        assert isinstance(data["provider"], str)
        assert data["provider"] in ("openai", "gemini")

    def test_model_is_string(self, client):
        data = client.get("/health").json()
        assert isinstance(data["model"], str)
        assert len(data["model"]) > 0

    def test_timestamp_is_iso_format(self, client):
        data = client.get("/health").json()
        assert "T" in data["timestamp"]  # Basic ISO format check


class TestRootEndpoint:
    """Tests for GET /"""

    def test_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_has_api_name(self, client):
        data = client.get("/").json()
        assert data["name"] == "CampusAI API"


class TestCollegesEndpoint:
    """Tests for GET /colleges"""

    def test_returns_200(self, client):
        response = client.get("/colleges")
        assert response.status_code == 200

    def test_returns_colleges_list(self, client):
        data = client.get("/colleges").json()
        assert "colleges" in data
        assert isinstance(data["colleges"], list)
        assert len(data["colleges"]) >= 20  # At least 20+ colleges

    def test_college_has_required_fields(self, client):
        data = client.get("/colleges").json()
        college = data["colleges"][0]
        assert "id" in college
        assert "name" in college
        assert "short" in college
