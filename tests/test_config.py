"""
test_config.py — Tests for core/config.py functions and constants.
"""

import os
from pathlib import Path

import pytest


# ── _is_valid_key ─────────────────────────────────────────────────────────────

class TestIsValidKey:
    def test_valid_key(self):
        from core.config import _is_valid_key
        assert _is_valid_key("sk-abc123") is True

    def test_empty_string(self):
        from core.config import _is_valid_key
        assert _is_valid_key("") is False

    def test_whitespace_only(self):
        from core.config import _is_valid_key
        assert _is_valid_key("   ") is False

    def test_placeholder_openai(self):
        from core.config import _is_valid_key
        assert _is_valid_key("your_openai_api_key_here") is False

    def test_placeholder_google(self):
        from core.config import _is_valid_key
        assert _is_valid_key("your_google_gemini_api_key_here") is False

    def test_valid_with_whitespace(self):
        from core.config import _is_valid_key
        assert _is_valid_key("  sk-abc123  ") is True

    def test_none_treated_as_empty(self):
        from core.config import _is_valid_key
        assert _is_valid_key(None) is False


# ── is_openai_configured ─────────────────────────────────────────────────────

class TestIsOpenAIConfigured:
    def test_returns_true_when_valid_key_set(self, monkeypatch):
        from core.config import is_openai_configured
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
        assert is_openai_configured() is True

    def test_returns_false_when_no_key(self, monkeypatch):
        from core.config import is_openai_configured
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        assert is_openai_configured() is False

    def test_returns_false_when_placeholder(self, monkeypatch):
        from core.config import is_openai_configured
        monkeypatch.setenv("OPENAI_API_KEY", "your_openai_api_key_here")
        assert is_openai_configured() is False


# ── is_google_configured ──────────────────────────────────────────────────────

class TestIsGoogleConfigured:
    def test_returns_true_when_valid_key_set(self, monkeypatch):
        from core.config import is_google_configured
        monkeypatch.setenv("GOOGLE_API_KEY", "AIzaSy-test123")
        assert is_google_configured() is True

    def test_returns_false_when_no_key(self, monkeypatch):
        from core.config import is_google_configured
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        assert is_google_configured() is False

    def test_returns_false_when_placeholder(self, monkeypatch):
        from core.config import is_google_configured
        monkeypatch.setenv("GOOGLE_API_KEY", "your_google_gemini_api_key_here")
        assert is_google_configured() is False


# ── is_any_api_configured ─────────────────────────────────────────────────────

class TestIsAnyAPIConfigured:
    def test_returns_true_when_openai_set(self, monkeypatch):
        from core.config import is_any_api_configured
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        assert is_any_api_configured() is True

    def test_returns_true_when_google_set(self, monkeypatch):
        from core.config import is_any_api_configured
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("GOOGLE_API_KEY", "AIzaSy-test123")
        assert is_any_api_configured() is True

    def test_returns_false_when_neither_set(self, monkeypatch):
        from core.config import is_any_api_configured
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        assert is_any_api_configured() is False


# ── get_active_provider ───────────────────────────────────────────────────────

class TestGetActiveProvider:
    def test_returns_openai_when_explicit(self, monkeypatch):
        from core.config import get_active_provider
        monkeypatch.setenv("LLM_PROVIDER", "openai")
        assert get_active_provider() == "openai"

    def test_returns_gemini_when_explicit(self, monkeypatch):
        from core.config import get_active_provider
        monkeypatch.setenv("LLM_PROVIDER", "gemini")
        assert get_active_provider() == "gemini"

    def test_defaults_to_openai_when_key_available(self, monkeypatch):
        from core.config import get_active_provider
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        assert get_active_provider() == "openai"

    def test_returns_gemini_when_only_google_key(self, monkeypatch):
        from core.config import get_active_provider
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("GOOGLE_API_KEY", "AIzaSy-test123")
        assert get_active_provider() == "gemini"

    def test_defaults_to_openai_when_no_keys(self, monkeypatch):
        from core.config import get_active_provider
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        assert get_active_provider() == "openai"


# ── Constants and Structure ───────────────────────────────────────────────────

class TestConstants:
    def test_colleges_is_list(self):
        from core.config import COLLEGES
        assert isinstance(COLLEGES, list)
        assert len(COLLEGES) > 0

    def test_college_map_matches_colleges(self):
        from core.config import COLLEGES, COLLEGE_MAP
        assert len(COLLEGE_MAP) == len(COLLEGES)
        for college in COLLEGES:
            assert college["id"] in COLLEGE_MAP

    def test_every_college_has_required_keys(self):
        from core.config import COLLEGES
        required_keys = {"id", "name", "short", "icon", "type", "location", "color"}
        for college in COLLEGES:
            missing = required_keys - set(college.keys())
            assert not missing, f"College {college.get('id', '?')} missing keys: {missing}"

    def test_indexed_colleges_subset_of_colleges(self):
        from core.config import COLLEGES, INDEXED_COLLEGE_IDS
        college_ids = {c["id"] for c in COLLEGES}
        assert INDEXED_COLLEGE_IDS.issubset(college_ids)

    def test_paths_are_path_objects(self):
        from core.config import ROOT, DATA_DIR, VECTOR_STORE_PATH
        assert isinstance(ROOT, Path)
        assert isinstance(DATA_DIR, Path)
        assert isinstance(VECTOR_STORE_PATH, Path)

    def test_data_dir_is_under_root(self):
        from core.config import ROOT, DATA_DIR
        assert DATA_DIR == ROOT / "data"
