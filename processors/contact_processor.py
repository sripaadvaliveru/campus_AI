"""
contact_processor.py — Processes the contacts CSV directory into structured text for the vector store.
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def process_contacts(filepath: Path) -> List[Dict[str, Any]]:
    """
    Read the contacts CSV and produce rich text documents for each contact
    and department-level summaries, ready for embedding.
    """
    documents = []

    if not filepath.exists():
        logger.warning(f"Contacts file not found: {filepath}")
        return documents

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # --- Individual contact cards ---
        for row in rows:
            text = (
                f"Staff Contact Information\n"
                f"Name: {row.get('name', 'N/A')}\n"
                f"Designation: {row.get('designation', 'N/A')}\n"
                f"Department: {row.get('department', 'N/A')}\n"
                f"Email: {row.get('email', 'N/A')}\n"
                f"Phone: {row.get('phone', 'N/A')}\n"
                f"Office Location: {row.get('office_location', 'N/A')}\n"
                f"Office Hours: {row.get('office_hours', 'N/A')}\n"
                f"Specialization / Area: {row.get('specialization', 'N/A')}"
            )
            documents.append({
                "text": text,
                "metadata": {
                    "source": "directory.csv",
                    "type": "contact",
                    "name": row.get("name", ""),
                    "department": row.get("department", ""),
                    "designation": row.get("designation", ""),
                }
            })

        # --- Department summaries ---
        departments: Dict[str, List[str]] = {}
        for row in rows:
            dept = row.get("department", "Unknown")
            departments.setdefault(dept, []).append(
                f"  • {row.get('name')} — {row.get('designation')} "
                f"| {row.get('email')} | {row.get('phone')}"
            )

        for dept, members in departments.items():
            dept_text = (
                f"Department Contact List: {dept}\n"
                f"Faculty and Staff in {dept}:\n"
                + "\n".join(members)
            )
            documents.append({
                "text": dept_text,
                "metadata": {
                    "source": "directory.csv",
                    "type": "department_summary",
                    "department": dept
                }
            })

        # --- Roles quick-reference ---
        key_roles = {
            "HoD": "Head of Department",
            "Dean": "Dean",
            "Registrar": "Registrar",
            "Warden": "Warden",
            "Librarian": "Librarian",
            "Placement": "Training & Placement",
            "Principal": "Principal",
            "Medical": "Medical Officer",
            "NSS": "NSS Officer",
            "NCC": "NCC Officer",
        }

        for keyword, role_label in key_roles.items():
            matched = [
                r for r in rows
                if keyword.lower() in r.get("designation", "").lower()
                or keyword.lower() in r.get("name", "").lower()
            ]
            if matched:
                lines = [f"Key Role — {role_label}:"]
                for r in matched:
                    lines.append(
                        f"  Name: {r.get('name')} | Dept: {r.get('department')} "
                        f"| Email: {r.get('email')} | Phone: {r.get('phone')}"
                    )
                documents.append({
                    "text": "\n".join(lines),
                    "metadata": {"source": "directory.csv", "type": "role_reference"}
                })

        logger.info(f"Processed {len(documents)} contact documents from {filepath.name}")

    except Exception as e:
        logger.error(f"Error processing contacts: {e}")

    return documents
