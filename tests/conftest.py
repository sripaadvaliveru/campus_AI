"""
conftest.py — Shared test fixtures for CampusAI test suite.
"""

import sqlite3
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Ensure project root is on sys.path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# SQL to create all tables
_CREATE_TABLES_SQL = """
    CREATE TABLE IF NOT EXISTS query_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        user_query TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        tool_used TEXT,
        category TEXT,
        timestamp TEXT NOT NULL,
        response_time_ms INTEGER
    );
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_id INTEGER REFERENCES query_history(id),
        rating INTEGER CHECK(rating IN (1, -1)),
        feedback_text TEXT,
        timestamp TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        total_queries INTEGER DEFAULT 0,
        positive_feedback INTEGER DEFAULT 0,
        negative_feedback INTEGER DEFAULT 0,
        top_categories TEXT,
        updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS cached_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_hash TEXT UNIQUE NOT NULL,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        created_at TEXT NOT NULL,
        hit_count INTEGER DEFAULT 0
    );
"""


@pytest.fixture(autouse=True)
def patch_db(tmp_path, monkeypatch):
    """Monkeypatch get_connection to use temp file SQLite for all DB tests."""
    db_path = str(tmp_path / "test_campus.db")
    # Initialize tables on a fresh connection
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(_CREATE_TABLES_SQL)
    conn.commit()
    conn.close()

    def _get_connection():
        c = sqlite3.connect(db_path)
        c.row_factory = sqlite3.Row
        return c

    monkeypatch.setattr("core.database.get_connection", _get_connection)


@pytest.fixture
def sample_contacts_csv(tmp_path):
    """Create a temporary contacts CSV file."""
    csv_content = (
        "name,designation,department,email,phone,office_location,office_hours,specialization\n"
        "Dr. Rajesh Kumar,Professor & HOD,Computer Science,rajesh@cbit.ac.in,9876543210,Block A Room 301,10:00-17:00,AI/ML\n"
        "Dr. Priya Sharma,Associate Professor,Electronics,priya@cbit.ac.in,9876543211,Block B Room 205,09:00-16:00,VLSI\n"
        "Mr. Venkat Admin,Office Administrator,Administration,admin@cbit.ac.in,9876543212,Admin Block,09:00-18:00,Admin\n"
    )
    contacts_dir = tmp_path / "data" / "contacts"
    contacts_dir.mkdir(parents=True)
    csv_file = contacts_dir / "directory.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    return csv_file


@pytest.fixture
def sample_events_json(tmp_path):
    """Create a temporary events JSON file."""
    import json
    events_data = {
        "odd_semester": {
            "name": "Odd Semester (Jul-Dec 2026)",
            "events": [
                {"event": "Semester Begins", "date": "2026-07-15", "category": "academic", "description": "Classes start"},
                {"event": "Mid-Term Exams", "date": "2026-09-01", "category": "exam", "description": "Mid-semester exams"},
                {"event": "Diwali Holiday", "date": "2026-10-20", "category": "holiday", "description": "Diwali break"},
            ],
        },
        "even_semester": {
            "name": "Even Semester (Jan-May 2027)",
            "events": [
                {"event": "Semester Begins", "date": "2027-01-05", "category": "academic", "description": "Classes start"},
                {"event": "Annual Day", "date": "2027-03-15", "category": "cultural", "description": "College annual day"},
            ],
        },
    }
    events_dir = tmp_path / "data" / "events"
    events_dir.mkdir(parents=True)
    events_file = events_dir / "academic_calendar.json"
    events_file.write_text(json.dumps(events_data), encoding="utf-8")
    return events_file


@pytest.fixture
def sample_facilities_json(tmp_path):
    """Create a temporary facilities JSON file."""
    import json
    facilities = {
        "library": {
            "name": "Central Library",
            "description": "24/7 library with 50k+ books",
            "timing": "24/7",
            "location": "Main Building Ground Floor",
        },
        "hostel": {
            "name": "Student Hostels",
            "description": "12 hostels for men and women",
            "timing": "Check-in: 6AM-10PM",
            "location": "Campus Periphery",
        },
    }
    campus_dir = tmp_path / "data" / "campus"
    campus_dir.mkdir(parents=True)
    fac_file = campus_dir / "facilities.json"
    fac_file.write_text(json.dumps(facilities), encoding="utf-8")
    return fac_file


@pytest.fixture
def sample_clubs_json(tmp_path):
    """Create a temporary clubs JSON file."""
    import json
    clubs = {
        "technical": [
            {"name": "Coding Club", "description": "Competitive programming and hackathons", "events": ["Hackfest", "Code Rush"]},
        ],
        "cultural": [
            {"name": "Drama Society", "description": "Theater and street plays", "events": ["Monoact", "Street Play"]},
        ],
    }
    campus_dir = tmp_path / "data" / "campus"
    campus_dir.mkdir(parents=True)
    clubs_file = campus_dir / "clubs_activities.json"
    clubs_file.write_text(json.dumps(clubs), encoding="utf-8")
    return clubs_file
