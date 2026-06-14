"""
calendar_processor.py — Processes the academic calendar JSON into
searchable text documents for the FAISS vector store.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def process_calendar(filepath: Path) -> List[Dict[str, Any]]:
    """
    Read the academic calendar JSON and produce event text documents
    plus deadline and placement calendar summaries.
    """
    documents = []

    if not filepath.exists():
        logger.warning(f"Calendar file not found: {filepath}")
        return documents

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        academic_year = data.get("academic_year", "")

        # --- Semester event documents ---
        for sem_key in ["odd_semester", "even_semester"]:
            sem = data.get(sem_key, {})
            sem_name = sem.get("name", sem_key)
            events = sem.get("events", [])

            if not events:
                continue

            # Individual event documents
            for ev in events:
                text = (
                    f"Academic Event: {ev.get('event', 'N/A')}\n"
                    f"Academic Year: {academic_year}\n"
                    f"Semester: {sem_name}\n"
                    f"Date: {ev.get('date', 'TBA')}\n"
                    f"Category: {ev.get('category', 'general').capitalize()}\n"
                    f"Details: {ev.get('description', 'No additional details.')}"
                )
                documents.append({
                    "text": text,
                    "metadata": {
                        "source": filepath.name,
                        "type": "calendar_event",
                        "date": ev.get("date", ""),
                        "category": ev.get("category", ""),
                        "semester": sem_key
                    }
                })

            # Semester overview summary
            categories: Dict[str, List[str]] = {}
            for ev in events:
                cat = ev.get("category", "general")
                categories.setdefault(cat, []).append(
                    f"  • {ev.get('date', 'TBA')} — {ev.get('event', '')}"
                )

            summary_parts = [f"Academic Calendar Summary: {sem_name} ({academic_year})"]
            for cat, ev_lines in categories.items():
                summary_parts.append(f"\n{cat.upper()} DATES:")
                summary_parts.extend(ev_lines)

            documents.append({
                "text": "\n".join(summary_parts),
                "metadata": {
                    "source": filepath.name,
                    "type": "semester_summary",
                    "semester": sem_key
                }
            })

        # --- Placement calendar ---
        placement_events = data.get("placement_calendar", {}).get("events", [])
        if placement_events:
            placement_text = "Campus Placement Calendar:\n"
            for ev in placement_events:
                placement_text += (
                    f"\n• {ev.get('period', '')}: {ev.get('event', '')}\n"
                    f"  {ev.get('description', '')}\n"
                )
            documents.append({
                "text": placement_text,
                "metadata": {"source": filepath.name, "type": "placement_calendar"}
            })

        # --- Important deadlines ---
        deadlines = data.get("important_deadlines", [])
        if deadlines:
            dl_text = "Important Academic Deadlines and Last Dates:\n"
            for dl in deadlines:
                dl_text += f"• {dl.get('deadline', '')}: {dl.get('description', '')}\n"
            documents.append({
                "text": dl_text,
                "metadata": {"source": filepath.name, "type": "deadlines"}
            })

        logger.info(f"Processed {len(documents)} calendar documents from {filepath.name}")

    except Exception as e:
        logger.error(f"Error processing calendar: {e}")

    return documents
