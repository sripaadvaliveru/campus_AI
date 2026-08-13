"""
data_loader.py — Shared data loading functions for contacts and events.
Used by both app.py and backend/main.py to avoid duplication.
"""

import json
import csv
import logging
from typing import List, Dict, Any

from core.config import DATA_DIR

logger = logging.getLogger(__name__)


def load_contacts() -> List[Dict[str, str]]:
    """Load contact directory from CSV."""
    try:
        contacts_file = DATA_DIR / "contacts" / "directory.csv"
        with open(contacts_file, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as e:
        logger.error(f"Error loading contacts: {e}")
        return []


def load_events() -> List[Dict[str, Any]]:
    """Load all events from the academic calendar."""
    try:
        cal_file = DATA_DIR / "events" / "academic_calendar.json"
        with open(cal_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        events = []
        for sem_key in ["odd_semester", "even_semester"]:
            sem = data.get(sem_key, {})
            for ev in sem.get("events", []):
                ev["semester"] = sem.get("name", "")
                events.append(ev)
        return sorted(events, key=lambda x: x.get("date", ""))
    except Exception as e:
        logger.error(f"Error loading events: {e}")
        return []
