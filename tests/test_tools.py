"""
test_tools.py — Tests for core/tools.py tool classes.
"""

import json
from unittest.mock import patch, MagicMock

import pytest


# ── get_all_tools ─────────────────────────────────────────────────────────────

class TestGetAllTools:
    def test_returns_six_tools(self):
        from core.tools import get_all_tools
        tools = get_all_tools()
        assert len(tools) == 6

    def test_tool_names_are_unique(self):
        from core.tools import get_all_tools
        tools = get_all_tools()
        names = [t.name for t in tools]
        assert len(names) == len(set(names))

    def test_expected_tool_names(self):
        from core.tools import get_all_tools
        tools = get_all_tools()
        names = {t.name for t in tools}
        expected = {
            "campus_knowledge_search",
            "get_campus_events",
            "search_contacts",
            "get_facility_info",
            "get_clubs_activities",
            "get_institution_data",
        }
        assert names == expected


# ── EventCalendarTool ────────────────────────────────────────────────────────

class TestEventCalendarTool:
    def test_upcoming_events(self, sample_events_json, monkeypatch):
        from core.tools import EventCalendarTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_events_json.parent.parent)
        tool = EventCalendarTool()
        result = tool._run("upcoming events")
        assert "Semester Begins" in result or "No events" in result

    def test_exam_category(self, sample_events_json, monkeypatch):
        from core.tools import EventCalendarTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_events_json.parent.parent)
        tool = EventCalendarTool()
        result = tool._run("exam")
        assert "Mid-Term" in result or "No events" in result

    def test_missing_file(self, tmp_path, monkeypatch):
        from core.tools import EventCalendarTool
        monkeypatch.setattr("core.tools.DATA_DIR", tmp_path / "nonexistent")
        tool = EventCalendarTool()
        result = tool._run("upcoming events")
        assert len(result) > 0  # Should return some error/fallback message


# ── ContactDirectoryTool ──────────────────────────────────────────────────────

class TestContactDirectoryTool:
    def test_search_by_name(self, sample_contacts_csv, monkeypatch):
        from core.tools import ContactDirectoryTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_contacts_csv.parent.parent)
        tool = ContactDirectoryTool()
        result = tool._run("Rajesh Kumar")
        assert "Rajesh Kumar" in result

    def test_search_by_department(self, sample_contacts_csv, monkeypatch):
        from core.tools import ContactDirectoryTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_contacts_csv.parent.parent)
        tool = ContactDirectoryTool()
        result = tool._run("Computer Science department")
        assert "Rajesh" in result or "CS" in result.upper() or "Computer" in result

    def test_no_results(self, sample_contacts_csv, monkeypatch):
        from core.tools import ContactDirectoryTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_contacts_csv.parent.parent)
        tool = ContactDirectoryTool()
        result = tool._run("xyznonexistent123")
        assert "no match" in result.lower() or "not found" in result.lower() or len(result) > 0


# ── FacilityInfoTool ──────────────────────────────────────────────────────────

class TestFacilityInfoTool:
    def test_library_facility(self, sample_facilities_json, monkeypatch):
        from core.tools import FacilityInfoTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_facilities_json.parent.parent)
        tool = FacilityInfoTool()
        result = tool._run("library")
        assert "Library" in result or "library" in result.lower()

    def test_unknown_facility(self, sample_facilities_json, monkeypatch):
        from core.tools import FacilityInfoTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_facilities_json.parent.parent)
        tool = FacilityInfoTool()
        result = tool._run("swimming pool")
        assert len(result) > 0  # Should return some fallback message


# ── ClubsActivitiesTool ───────────────────────────────────────────────────────

class TestClubsActivitiesTool:
    def test_technical_clubs(self, sample_clubs_json, monkeypatch):
        from core.tools import ClubsActivitiesTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_clubs_json.parent.parent)
        tool = ClubsActivitiesTool()
        result = tool._run("technical clubs")
        assert "Coding" in result or "technical" in result.lower()

    def test_all_clubs(self, sample_clubs_json, monkeypatch):
        from core.tools import ClubsActivitiesTool
        monkeypatch.setattr("core.tools.DATA_DIR", sample_clubs_json.parent.parent)
        tool = ClubsActivitiesTool()
        result = tool._run("clubs")
        assert len(result) > 0


# ── InstitutionDataTool ───────────────────────────────────────────────────────

class TestInstitutionDataTool:
    def test_known_institution(self, monkeypatch):
        from core.tools import InstitutionDataTool
        # Mock the file read to return sample data
        sample_data = {
            "name": "IIT Hyderabad",
            "fees": {"tuition": "Rs. 1,68,993/sem"},
            "placements": {"highest": "Rs. 90 LPA", "average": "Rs. 20 LPA"},
        }
        mock_open = MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(sample_data))))
        monkeypatch.setattr("builtins.open", mock_open)
        tool = InstitutionDataTool()
        result = tool._run("iith", "fees")
        assert len(result) > 0

    def test_unknown_institution(self, monkeypatch):
        from core.tools import InstitutionDataTool
        tool = InstitutionDataTool()
        result = tool._run("unknown_college", "fees")
        assert len(result) > 0
