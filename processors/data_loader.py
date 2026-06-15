"""
data_loader.py — Loads JSON and CSV campus data files and converts them
to text chunks suitable for embedding into the FAISS vector store.
"""

import json
import csv
import os
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"


def _flatten_json(obj: Any, prefix: str = "") -> List[str]:
    """Recursively flatten a nested JSON object into readable text chunks."""
    chunks = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            section_title = f"{prefix} > {key}".strip(" >") if prefix else key
            if isinstance(value, (dict, list)):
                chunks.extend(_flatten_json(value, section_title))
            else:
                chunks.append(f"{section_title}: {value}")

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                chunks.extend(_flatten_json(item, prefix))
            else:
                chunks.append(f"{prefix}: {item}")

    return chunks


def _chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> List[str]:
    """Split a long text into overlapping chunks."""
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def load_json_file(filepath: Path) -> List[Dict[str, Any]]:
    """Load a JSON file and return list of document dicts with text + metadata."""
    documents = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        flat_chunks = _flatten_json(data)
        # Group chunks into larger meaningful blocks
        block = ""
        for chunk in flat_chunks:
            if len(block) + len(chunk) < 600:
                block += "\n" + chunk
            else:
                if block.strip():
                    documents.append({
                        "text": block.strip(),
                        "metadata": {
                            "source": filepath.name,
                            "type": "campus_data"
                        }
                    })
                block = chunk

        if block.strip():
            documents.append({
                "text": block.strip(),
                "metadata": {
                    "source": filepath.name,
                    "type": "campus_data"
                }
            })

        logger.info(f"Loaded {len(documents)} chunks from {filepath.name}")
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")

    return documents


def load_csv_contacts(filepath: Path) -> List[Dict[str, Any]]:
    """Load contacts CSV and convert each row to a searchable text document."""
    documents = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Create individual contact cards
        for row in rows:
            text = (
                f"Contact: {row.get('name', 'N/A')}\n"
                f"Designation: {row.get('designation', 'N/A')}\n"
                f"Department: {row.get('department', 'N/A')}\n"
                f"Email: {row.get('email', 'N/A')}\n"
                f"Phone: {row.get('phone', 'N/A')}\n"
                f"Office Location: {row.get('office_location', 'N/A')}\n"
                f"Office Hours: {row.get('office_hours', 'N/A')}\n"
                f"Specialization: {row.get('specialization', 'N/A')}"
            )
            documents.append({
                "text": text,
                "metadata": {
                    "source": "directory.csv",
                    "type": "contact",
                    "name": row.get("name", ""),
                    "department": row.get("department", "")
                }
            })

        # Also create department summaries
        departments: Dict[str, List[str]] = {}
        for row in rows:
            dept = row.get("department", "Unknown")
            if dept not in departments:
                departments[dept] = []
            departments[dept].append(
                f"  - {row.get('name')} ({row.get('designation')}): {row.get('email')} | {row.get('phone')}"
            )

        for dept, members in departments.items():
            dept_text = f"Department: {dept}\nMembers:\n" + "\n".join(members)
            documents.append({
                "text": dept_text,
                "metadata": {
                    "source": "directory.csv",
                    "type": "department_summary",
                    "department": dept
                }
            })

        logger.info(f"Loaded {len(documents)} contact documents from {filepath.name}")
    except Exception as e:
        logger.error(f"Error loading contacts CSV: {e}")

    return documents


def load_events_calendar(filepath: Path) -> List[Dict[str, Any]]:
    """Load events calendar JSON and create searchable event documents."""
    documents = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Process odd and even semester events
        for sem_key in ["odd_semester", "even_semester"]:
            sem = data.get(sem_key, {})
            sem_name = sem.get("name", sem_key)
            events = sem.get("events", [])

            for event in events:
                text = (
                    f"Event: {event.get('event', 'N/A')}\n"
                    f"Semester: {sem_name}\n"
                    f"Date: {event.get('date', 'N/A')}\n"
                    f"Category: {event.get('category', 'N/A')}\n"
                    f"Description: {event.get('description', 'N/A')}"
                )
                documents.append({
                    "text": text,
                    "metadata": {
                        "source": filepath.name,
                        "type": "event",
                        "date": event.get("date", ""),
                        "category": event.get("category", "")
                    }
                })

        # Process placement calendar
        placement_events = data.get("placement_calendar", {}).get("events", [])
        for ev in placement_events:
            text = (
                f"Placement Event: {ev.get('event', 'N/A')}\n"
                f"Period: {ev.get('period', 'N/A')}\n"
                f"Description: {ev.get('description', 'N/A')}"
            )
            documents.append({
                "text": text,
                "metadata": {
                    "source": filepath.name,
                    "type": "placement_event"
                }
            })

        # Process deadlines
        deadlines = data.get("important_deadlines", [])
        deadline_text = "Important Academic Deadlines:\n"
        for dl in deadlines:
            deadline_text += f"- {dl.get('deadline')}: {dl.get('description')}\n"
        if deadlines:
            documents.append({
                "text": deadline_text,
                "metadata": {"source": filepath.name, "type": "deadlines"}
            })

        logger.info(f"Loaded {len(documents)} event documents from {filepath.name}")
    except Exception as e:
        logger.error(f"Error loading calendar: {e}")

    return documents


def load_all_data() -> List[Dict[str, Any]]:
    """Load all campus data files and return combined list of documents."""
    all_docs = []

    # Load JSON data files
    json_files = [
        DATA_DIR / "campus" / "facilities.json",
        DATA_DIR / "campus" / "general_info.json",
        DATA_DIR / "campus" / "clubs_activities.json",
        DATA_DIR / "campus" / "procedures.json",
        DATA_DIR / "campus" / "college_types.json",
    ]

    for json_file in json_files:
        if json_file.exists():
            docs = load_json_file(json_file)
            all_docs.extend(docs)
        else:
            logger.warning(f"File not found: {json_file}")

    # Load contacts
    contacts_file = DATA_DIR / "contacts" / "directory.csv"
    if contacts_file.exists():
        all_docs.extend(load_csv_contacts(contacts_file))

    # Load events calendar
    calendar_file = DATA_DIR / "events" / "academic_calendar.json"
    if calendar_file.exists():
        all_docs.extend(load_events_calendar(calendar_file))

    # Load Hyderabad-specific institution data (IITH, IIITH, NALSAR, HCU, OU, BITS, NIRF)
    hyderabad_dir = DATA_DIR / "hyderabad"
    if hyderabad_dir.exists():
        # Load JSON files
        json_files = list(hyderabad_dir.glob("*.json"))
        for hyd_file in json_files:
            docs = load_json_file(hyd_file)
            all_docs.extend(docs)
            logger.info(f"Loaded {len(docs)} chunks from Hyderabad JSON: {hyd_file.name}")

        # Load Markdown and Text files
        txt_files = list(hyderabad_dir.glob("*.md")) + list(hyderabad_dir.glob("*.txt"))
        for txt_file in txt_files:
            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    content = f.read()
                # Split content into 600 character chunks with 100 character overlap
                chunks = _chunk_text(content, chunk_size=600, overlap=100)
                for chunk in chunks:
                    all_docs.append({
                        "text": chunk.strip(),
                        "metadata": {
                            "source": txt_file.name,
                            "type": "campus_report"
                        }
                    })
                logger.info(f"Loaded {len(chunks)} chunks from Hyderabad report: {txt_file.name}")
            except Exception as e:
                logger.error(f"Error loading text file {txt_file.name}: {e}")

    logger.info(f"Total documents loaded: {len(all_docs)}")
    return all_docs



def get_raw_contacts() -> List[Dict[str, str]]:
    """Return raw contact rows as dicts for the contact search tool."""
    contacts = []
    filepath = DATA_DIR / "contacts" / "directory.csv"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            contacts = list(reader)
    except Exception as e:
        logger.error(f"Error reading contacts: {e}")
    return contacts


def get_raw_events() -> List[Dict[str, str]]:
    """Return raw event list for the events tool."""
    events = []
    filepath = DATA_DIR / "events" / "academic_calendar.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for sem_key in ["odd_semester", "even_semester"]:
            sem = data.get(sem_key, {})
            for ev in sem.get("events", []):
                ev["semester"] = sem.get("name", "")
                events.append(ev)
    except Exception as e:
        logger.error(f"Error reading events: {e}")
    return events
