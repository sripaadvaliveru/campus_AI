"""
test_data_loader.py — Tests for core/data_loader.py functions.
"""

import json

import pytest


# ── load_contacts ─────────────────────────────────────────────────────────────

class TestLoadContacts:
    def test_loads_contacts_from_csv(self, sample_contacts_csv, monkeypatch):
        from core.data_loader import load_contacts
        monkeypatch.setattr("core.data_loader.DATA_DIR", sample_contacts_csv.parent.parent)
        contacts = load_contacts()
        assert len(contacts) == 3
        assert contacts[0]["name"] == "Dr. Rajesh Kumar"
        assert contacts[0]["department"] == "Computer Science"

    def test_returns_empty_on_missing_file(self, tmp_path, monkeypatch):
        from core.data_loader import load_contacts
        monkeypatch.setattr("core.data_loader.DATA_DIR", tmp_path / "nonexistent")
        contacts = load_contacts()
        assert contacts == []

    def test_returns_list_of_dicts(self, sample_contacts_csv, monkeypatch):
        from core.data_loader import load_contacts
        monkeypatch.setattr("core.data_loader.DATA_DIR", sample_contacts_csv.parent.parent)
        contacts = load_contacts()
        assert all(isinstance(c, dict) for c in contacts)


# ── load_events ───────────────────────────────────────────────────────────────

class TestLoadEvents:
    def test_loads_events_from_json(self, sample_events_json, monkeypatch):
        from core.data_loader import load_events
        monkeypatch.setattr("core.data_loader.DATA_DIR", sample_events_json.parent.parent)
        events = load_events()
        assert len(events) == 5  # 3 odd + 2 even

    def test_events_sorted_by_date(self, sample_events_json, monkeypatch):
        from core.data_loader import load_events
        monkeypatch.setattr("core.data_loader.DATA_DIR", sample_events_json.parent.parent)
        events = load_events()
        dates = [e["date"] for e in events]
        assert dates == sorted(dates)

    def test_semester_field_added(self, sample_events_json, monkeypatch):
        from core.data_loader import load_events
        monkeypatch.setattr("core.data_loader.DATA_DIR", sample_events_json.parent.parent)
        events = load_events()
        for event in events:
            assert "semester" in event

    def test_returns_empty_on_missing_file(self, tmp_path, monkeypatch):
        from core.data_loader import load_events
        monkeypatch.setattr("core.data_loader.DATA_DIR", tmp_path / "nonexistent")
        events = load_events()
        assert events == []
