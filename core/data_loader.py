"""
data_loader.py — Shared data loading functions for contacts and events.
Used by both app.py and backend/main.py to avoid duplication.
Supports college-specific data files with fallback to generic data.
"""

import json
import csv
import logging
from typing import List, Dict, Any, Optional

from core.config import DATA_DIR

logger = logging.getLogger(__name__)

# Colleges that have their own data files
INDEXED_DATA_COLLEGES = {
    "iith", "iiith", "nalsar", "nims", "hcu", "osmania", "bits_hyd",
}


def load_contacts(college_id: Optional[str] = None) -> List[Dict[str, str]]:
    """Load contact directory from CSV.
    
    Tries college-specific file first (e.g., data/contacts/iith_directory.csv),
    falls back to generic data/contacts/directory.csv.
    """
    try:
        # Try college-specific file
        if college_id and college_id in INDEXED_DATA_COLLEGES:
            college_file = DATA_DIR / "contacts" / f"{college_id}_directory.csv"
            if college_file.exists():
                with open(college_file, "r", encoding="utf-8") as f:
                    return list(csv.DictReader(f))

        # Fall back to generic
        contacts_file = DATA_DIR / "contacts" / "directory.csv"
        with open(contacts_file, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as e:
        logger.error(f"Error loading contacts: {e}")
        return []


def load_events(college_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load all events from the academic calendar.
    
    Tries college-specific file first (e.g., data/events/iith_calendar.json),
    falls back to generic data/events/academic_calendar.json.
    """
    try:
        # Try college-specific file
        if college_id and college_id in INDEXED_DATA_COLLEGES:
            college_file = DATA_DIR / "events" / f"{college_id}_calendar.json"
            if college_file.exists():
                with open(college_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return _parse_calendar_events(data)

        # Fall back to generic
        cal_file = DATA_DIR / "events" / "academic_calendar.json"
        with open(cal_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _parse_calendar_events(data)
    except Exception as e:
        logger.error(f"Error loading events: {e}")
        return []


def _parse_calendar_events(data: dict) -> List[Dict[str, Any]]:
    """Parse events from a calendar JSON structure."""
    events = []
    for sem_key in ["odd_semester", "even_semester"]:
        sem = data.get(sem_key, {})
        for ev in sem.get("events", []):
            ev["semester"] = sem.get("name", "")
            events.append(ev)
    return sorted(events, key=lambda x: x.get("date", ""))
