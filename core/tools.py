"""
tools.py — Five custom LangChain tools for the Campus Info Chatbot agent.
Each tool serves a distinct campus information domain.
"""

import json
import logging
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pathlib import Path

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"


# ─────────────────────────────────────────────────────────────────────────────
# Tool 1: Campus Knowledge RAG Search
# ─────────────────────────────────────────────────────────────────────────────

class CampusKnowledgeInput(BaseModel):
    query: str = Field(description="The question or topic to search in campus knowledge base")


class CampusKnowledgeTool(BaseTool):
    """Tool to search the campus knowledge base using semantic vector search."""

    name: str = "campus_knowledge_search"
    description: str = (
        "Search the comprehensive campus knowledge base for information about: "
        "academic regulations, attendance policies, examination patterns, grading systems, "
        "CGPA/SGPA calculation, Osmania University CBCS rules, NIRF rankings, "
        "scholarships, certificates (bonafide, TC, migration), "
        "admission procedures, college types (engineering/medical/arts/management/law), "
        "hostel rules, library services, facilities, and student procedures. "
        "Also covers IIT Hyderabad, IIIT Hyderabad, BITS Pilani, NALSAR, NIMS, HCU, Osmania University, "
        "Nizam College, St. Francis College, IMT Hyderabad, IBS Hyderabad, Osmania Medical College, and ISB Hyderabad. "
        "Use this tool for most campus information questions."

    )
    args_schema: type = CampusKnowledgeInput

    def _run(self, query: str) -> str:
        try:
            from core.embeddings import get_vector_store
            vs = get_vector_store()
            if not vs.is_ready:
                return "Knowledge base not yet initialized. Please run initialize.py first."
            context = vs.get_relevant_context(query, top_k=8)
            return f"Relevant campus information:\n\n{context}"
        except Exception as e:
            logger.error(f"CampusKnowledgeTool error: {e}")
            return f"Error searching knowledge base: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────────
# Tool 2: Events & Academic Calendar
# ─────────────────────────────────────────────────────────────────────────────

class EventsInput(BaseModel):
    query: str = Field(description="Type of events to search: 'upcoming', 'exam', 'cultural', 'sports', 'placement', 'holiday', or a specific month/date")


class EventCalendarTool(BaseTool):
    """Tool to query the academic calendar and campus events."""

    name: str = "get_campus_events"
    description: str = (
        "Get information about campus events, academic calendar, important dates and deadlines. "
        "Use for questions about: upcoming events, exams, cultural fests, sports meets, "
        "placement drives, holidays, semester start/end dates, internal assessment dates, "
        "convocation, freshers party, and other scheduled activities."
    )
    args_schema: type = EventsInput

    def _run(self, query: str) -> str:
        try:
            calendar_file = DATA_DIR / "events" / "academic_calendar.json"
            if not calendar_file.exists():
                return "Calendar data not found."

            with open(calendar_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            query_lower = query.lower()
            today = date.today()

            all_events = []
            for sem_key in ["odd_semester", "even_semester"]:
                sem = data.get(sem_key, {})
                sem_name = sem.get("name", "")
                for ev in sem.get("events", []):
                    ev["semester"] = sem_name
                    all_events.append(ev)

            # Filter by category or keyword
            category_map = {
                "exam": ["exam", "internal", "assessment", "ia-", "end semester", "supplementary", "viva"],
                "cultural": ["cultural", "fest", "music", "dance", "drama", "freshers", "party"],
                "sports": ["sports", "athletic", "cricket", "football", "basketball"],
                "placement": ["placement", "recruit", "campus drive", "company"],
                "holiday": ["holiday", "diwali", "dussehra", "pongal", "independence", "republic", "christmas"],
                "upcoming": ["upcoming", "next", "soon", "future"],
                "all": []
            }

            matched_category = None
            for cat, keywords in category_map.items():
                if any(kw in query_lower for kw in keywords) or cat in query_lower:
                    matched_category = cat
                    break

            if matched_category == "upcoming":
                # Show next 5 future events
                future_events = [
                    ev for ev in all_events
                    if ev.get("date") and ev["date"] >= today.isoformat()
                ]
                future_events.sort(key=lambda x: x.get("date", ""))
                filtered = future_events[:5]
            elif matched_category and matched_category != "all":
                keywords = category_map[matched_category]
                filtered = [
                    ev for ev in all_events
                    if any(kw in ev.get("event", "").lower() or kw in ev.get("category", "").lower()
                           for kw in keywords)
                ]
            else:
                # Keyword search across all events
                filtered = [
                    ev for ev in all_events
                    if any(word in ev.get("event", "").lower() or word in ev.get("description", "").lower()
                           for word in query_lower.split() if len(word) > 3)
                ][:8]

            if not filtered:
                filtered = all_events[:5]
                prefix = "Here are some upcoming events (no exact match found):\n"
            else:
                prefix = f"Campus events matching '{query}':\n"

            lines = [prefix]
            for ev in filtered:
                lines.append(
                    f"📅 {ev.get('event', 'Event')}\n"
                    f"   Date: {ev.get('date', 'TBA')} | Category: {ev.get('category', '').capitalize()}\n"
                    f"   {ev.get('description', '')}\n"
                )

            # Also include important deadlines if relevant
            if "deadline" in query_lower or "last date" in query_lower:
                deadlines = data.get("important_deadlines", [])
                if deadlines:
                    lines.append("\n⏰ Important Deadlines:")
                    for dl in deadlines[:5]:
                        lines.append(f"   • {dl.get('deadline')}: {dl.get('description')}")

            return "\n".join(lines)

        except Exception as e:
            logger.error(f"EventCalendarTool error: {e}")
            return f"Error retrieving events: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────────
# Tool 3: Contact Directory Search
# ─────────────────────────────────────────────────────────────────────────────

class ContactInput(BaseModel):
    query: str = Field(description="Name, department, designation, or role to search for (e.g. 'HOD CSE', 'placement officer', 'warden', 'library')")


class ContactDirectoryTool(BaseTool):
    """Tool to search the faculty and staff contact directory."""

    name: str = "search_contacts"
    description: str = (
        "Search the campus contact directory for faculty, staff, and department contacts. "
        "Use for questions about: HOD contact, department faculty, placement officer, "
        "warden, librarian, dean, registrar, accounts office, exam cell, IT support, "
        "NSS officer, security, medical officer, and any staff/faculty contact info."
    )
    args_schema: type = ContactInput

    def _run(self, query: str) -> str:
        try:
            import csv
            contacts_file = DATA_DIR / "contacts" / "directory.csv"
            if not contacts_file.exists():
                return "Contact directory not found."

            with open(contacts_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                contacts = list(reader)

            query_lower = query.lower()
            query_words = [w for w in query_lower.split() if len(w) > 2]

            matched = []
            for contact in contacts:
                score = 0
                searchable = " ".join([
                    contact.get("name", ""),
                    contact.get("designation", ""),
                    contact.get("department", ""),
                    contact.get("specialization", "")
                ]).lower()

                for word in query_words:
                    if word in searchable:
                        score += 1

                if score > 0:
                    matched.append((score, contact))

            matched.sort(key=lambda x: x[0], reverse=True)
            top_results = [c for _, c in matched[:5]]

            if not top_results:
                # Fallback: return all departments overview
                departments = list(set(c.get("department", "") for c in contacts))[:8]
                return (
                    f"No contact found for '{query}'. Available departments include:\n"
                    + "\n".join(f"  • {d}" for d in departments)
                    + "\n\nTry searching by department name or role (e.g., 'HOD CSE', 'placement officer')."
                )

            lines = [f"📋 Contact Information (search: '{query}'):\n"]
            for c in top_results:
                lines.append(
                    f"👤 {c.get('name', 'N/A')}\n"
                    f"   Designation: {c.get('designation', 'N/A')}\n"
                    f"   Department: {c.get('department', 'N/A')}\n"
                    f"   📧 Email: {c.get('email', 'N/A')}\n"
                    f"   📞 Phone: {c.get('phone', 'N/A')}\n"
                    f"   🏢 Office: {c.get('office_location', 'N/A')}\n"
                    f"   🕐 Hours: {c.get('office_hours', 'N/A')}\n"
                )

            return "\n".join(lines)

        except Exception as e:
            logger.error(f"ContactDirectoryTool error: {e}")
            return f"Error searching contacts: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────────
# Tool 4: Facility Information
# ─────────────────────────────────────────────────────────────────────────────

class FacilityInput(BaseModel):
    facility_name: str = Field(description="Name of the facility to get info about (e.g., 'library', 'hostel', 'canteen', 'sports', 'medical', 'placement', 'transport', 'wifi', 'bank')")


class FacilityInfoTool(BaseTool):
    """Tool to get detailed campus facility information."""

    name: str = "get_facility_info"
    description: str = (
        "Get detailed information about campus facilities and their services. "
        "Use for questions about: library timings/services, hostel rules/facilities, "
        "canteen/cafeteria, sports complex, medical/health center, placement cell, "
        "computer labs, transport/bus service, WiFi, bank/ATM, auditorium booking, "
        "student center, and all other physical campus facilities."
    )
    args_schema: type = FacilityInput

    def _run(self, facility_name: str) -> str:
        try:
            facilities_file = DATA_DIR / "campus" / "facilities.json"
            if not facilities_file.exists():
                return "Facilities data not found."

            with open(facilities_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            facilities = data.get("facilities", {})
            query_lower = facility_name.lower()

            # Map keywords to facility keys
            facility_aliases = {
                "library": ["library", "book", "read", "n-list", "journal", "digital"],
                "hostel": ["hostel", "dormitory", "dorm", "accommodation", "residence", "mess", "warden"],
                "canteen_cafeteria": ["canteen", "cafeteria", "food", "eat", "mess", "meal"],
                "sports_complex": ["sport", "gym", "cricket", "football", "basketball", "badminton", "athletics"],
                "medical_center": ["medical", "health", "doctor", "hospital", "clinic", "ambulance", "nurse"],
                "placement_cell": ["placement", "recruit", "job", "career", "internship", "t&p", "training"],
                "computer_labs": ["computer", "lab", "pc", "internet", "software", "matlab", "programming"],
                "library_digital": ["nptel", "swayam", "mooc", "coursera", "digital", "online course", "ieee"],
                "transport": ["transport", "bus", "route", "shuttle", "commute", "travel"],
                "wifi_internet": ["wifi", "wi-fi", "internet", "network", "connect"],
                "bank_atm": ["bank", "atm", "sbi", "account", "scholarship payment"],
                "student_center": ["student center", "activity centre", "common room", "stationery"],
                "auditorium_seminar_halls": ["auditorium", "seminar", "hall", "booking", "event space"]
            }

            matched_key = None
            best_match = 0
            for key, aliases in facility_aliases.items():
                match_score = sum(1 for alias in aliases if alias in query_lower)
                if match_score > best_match:
                    best_match = match_score
                    matched_key = key

            if matched_key and matched_key in facilities:
                facility_data = facilities[matched_key]
                return self._format_facility(matched_key, facility_data)
            else:
                # List all facilities
                available = list(facilities.keys())
                return (
                    f"Facility '{facility_name}' not found. Available facilities:\n"
                    + "\n".join(f"  • {k.replace('_', ' ').title()}" for k in available)
                    + "\n\nPlease search for a specific facility."
                )

        except Exception as e:
            logger.error(f"FacilityInfoTool error: {e}")
            return f"Error retrieving facility info: {str(e)}"

    def _format_facility(self, key: str, data: dict) -> str:
        """Format facility data into a readable string."""
        title = key.replace("_", " ").title()
        lines = [f"🏛️ {title}\n{'─' * 40}"]

        for field, value in data.items():
            if isinstance(value, list):
                lines.append(f"\n{field.replace('_', ' ').title()}:")
                for item in value:
                    lines.append(f"  • {item}")
            elif isinstance(value, dict):
                lines.append(f"\n{field.replace('_', ' ').title()}:")
                for sub_key, sub_val in value.items():
                    if isinstance(sub_val, list):
                        lines.append(f"  {sub_key}:")
                        for si in sub_val:
                            lines.append(f"    - {si}")
                    else:
                        lines.append(f"  {sub_key}: {sub_val}")
            else:
                lines.append(f"\n{field.replace('_', ' ').title()}: {value}")

        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Tool 5: Clubs & Activities
# ─────────────────────────────────────────────────────────────────────────────

class ClubInput(BaseModel):
    query: str = Field(description="Type of club or activity to search: club name, category (technical/cultural/sports/social), or 'all'")


class ClubsActivitiesTool(BaseTool):
    """Tool to get information about campus clubs and student activities."""

    name: str = "get_clubs_activities"
    description: str = (
        "Get information about campus clubs, student organizations, and activities. "
        "Use for questions about: coding club, robotics, IEEE, drama, dance, music, "
        "NSS, NCC, sports teams, cultural fest, student council, entrepreneurship cell, "
        "how to join clubs, club activities, annual events, freshers party details."
    )
    args_schema: type = ClubInput

    def _run(self, query: str) -> str:
        try:
            clubs_file = DATA_DIR / "campus" / "clubs_activities.json"
            if not clubs_file.exists():
                return "Clubs data not found."

            with open(clubs_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            clubs_data = data.get("clubs_and_activities", {})
            query_lower = query.lower()

            category_map = {
                "technical": clubs_data.get("technical_clubs", []),
                "cultural": clubs_data.get("cultural_clubs", []),
                "sports": clubs_data.get("sports_clubs", []),
                "social": clubs_data.get("social_service", []),
                "governance": clubs_data.get("student_governance", []),
            }

            # Check if searching for a specific category
            matched_category = None
            for cat in category_map:
                if cat in query_lower:
                    matched_category = cat
                    break

            # Also check for keyword matches
            keyword_to_cat = {
                "coding": "technical", "programming": "technical", "robotics": "technical",
                "ieee": "technical", "web": "technical", "ml": "technical", "ai": "technical",
                "startup": "technical", "ecell": "technical",
                "music": "cultural", "dance": "cultural", "drama": "cultural",
                "theatre": "cultural", "art": "cultural", "literary": "cultural",
                "quiz": "cultural", "writing": "cultural",
                "cricket": "sports", "football": "sports", "basketball": "sports",
                "badminton": "sports", "chess": "sports", "athletics": "sports",
                "nss": "social", "ncc": "social", "rotaract": "social", "blood": "social",
                "student council": "governance", "union": "governance", "election": "governance",
                "anti-ragging": "governance", "posh": "governance"
            }

            for keyword, cat in keyword_to_cat.items():
                if keyword in query_lower:
                    matched_category = cat
                    break

            events_keywords = ["fest", "event", "annual", "cultural fest", "technical fest", "sports meet", "freshers"]

            if any(kw in query_lower for kw in events_keywords):
                events = clubs_data.get("major_annual_events", [])
                lines = ["🎉 Major Annual Campus Events:\n"]
                for ev in events:
                    lines.append(
                        f"📌 {ev.get('name', 'Event')}\n"
                        f"   Timing: {ev.get('timing', 'TBA')}\n"
                        f"   {ev.get('description', '')}\n"
                    )
                return "\n".join(lines)

            if matched_category and matched_category in category_map:
                clubs = category_map[matched_category]
                lines = [f"🎯 {matched_category.title()} Clubs & Organizations:\n"]
                for club in clubs:
                    lines.append(
                        f"📌 {club.get('name', 'Club')}\n"
                        f"   Activities: {', '.join(club.get('activities', [])[:3])}\n"
                        f"   How to Join: {club.get('how_to_join', 'Contact club coordinator')}\n"
                        + (f"   Benefits: {club.get('benefits', '')}\n" if club.get('benefits') else "")
                    )
                return "\n".join(lines)

            # Keyword search across all clubs
            all_clubs = []
            for cat_clubs in category_map.values():
                all_clubs.extend(cat_clubs)

            matched_clubs = []
            for club in all_clubs:
                club_text = json.dumps(club).lower()
                if any(word in club_text for word in query_lower.split() if len(word) > 3):
                    matched_clubs.append(club)

            if matched_clubs:
                lines = [f"🔍 Clubs matching '{query}':\n"]
                for club in matched_clubs[:4]:
                    lines.append(
                        f"📌 {club.get('name', 'Club')}\n"
                        f"   Activities: {', '.join(club.get('activities', [])[:3])}\n"
                        f"   How to Join: {club.get('how_to_join', 'Contact coordinator')}\n"
                    )
                return "\n".join(lines)

            # Default: show all categories
            return (
                "Available club categories on campus:\n"
                "  🔧 Technical: Coding, Robotics, IEEE, AI/ML, Web Dev, E-Cell\n"
                "  🎭 Cultural: Music, Dance, Drama, Fine Arts, Literary/Quill\n"
                "  ⚽ Sports: Cricket, Football, Basketball, Badminton, Chess\n"
                "  🤝 Social Service: NSS, NCC, Rotaract, Red Cross\n"
                "  🏛️ Governance: Student Council, Anti-Ragging, ICC/POSH\n\n"
                "Ask about any specific club for more details!"
            )

        except Exception as e:
            logger.error(f"ClubsActivitiesTool error: {e}")
            return f"Error retrieving clubs info: {str(e)}"



# ─────────────────────────────────────────────────────────────────────────────
# Tool 6: Direct Institution Data (Fees, Admissions, Placements)
# ─────────────────────────────────────────────────────────────────────────────

INSTITUTION_FILE_MAP = {
    "iith":     "iith.json",
    "iiith":    "iiith.json",
    "nalsar":   "other_institutions.json",
    "nims":     "other_institutions.json",
    "hcu":      "other_institutions.json",
    "osmania":  "other_institutions.json",
    "bits_hyd": "other_institutions.json",
    "nirf":     "nirf_rankings.json",
}

INSTITUTION_KEY_MAP = {
    "nalsar":   "NALSAR_University_of_Law",
    "nims":     "NIMS_Medical_Sciences",
    "hcu":      "University_of_Hyderabad_HCU",
    "osmania":  "Osmania_University_CBCS",
    "bits_hyd": "BITS_Pilani_Hyderabad",
}


class InstitutionDataInput(BaseModel):
    institution: str = Field(
        description="Institution ID: 'iith', 'iiith', 'nalsar', 'nims', 'hcu', 'osmania', 'bits_hyd', or 'nirf'"
    )
    topic: str = Field(
        description="Topic to retrieve: 'fees', 'admissions', 'placements', 'scholarships', 'hostel', 'transport', 'facilities', 'programs', 'cutoffs', 'all'"
    )


class InstitutionDataTool(BaseTool):
    """Tool to retrieve exact, structured data for specific Hyderabad institutions."""

    name: str = "get_institution_data"
    description: str = (
        "Get EXACT structured data (fee tables, admission details, placement stats, scholarships) "
        "for specific institutions. Use this tool when the user asks about: "
        "fee structure, tuition fees, hostel fees, exact placement packages, NEET/CLAT/JEE cutoffs, "
        "scholarship amounts, bus routes/timings, supercomputer specs, dining options, hostel rules, "
        "or any specific factual data from IIT Hyderabad (iith), IIIT Hyderabad (iiith), "
        "NALSAR (nalsar), NIMS (nims), University of Hyderabad (hcu), Osmania University (osmania), "
        "BITS Pilani Hyderabad (bits_hyd), or NIRF Rankings (nirf). "
        "Always prefer this tool over campus_knowledge_search for fee/admission/placement queries "
        "about these specific institutions."
    )
    args_schema: type = InstitutionDataInput

    def _run(self, institution: str, topic: str) -> str:
        try:
            hyd_dir = DATA_DIR / "hyderabad"
            inst_id = institution.lower().strip()
            topic_lower = topic.lower().strip()

            filename = INSTITUTION_FILE_MAP.get(inst_id)
            if not filename:
                return (
                    f"Institution '{institution}' not found. "
                    f"Valid structured options: iith, iiith, nalsar, nims, hcu, osmania, bits_hyd, nirf. "
                    f"For Nizam (nizam), St. Francis (st_francis), IMT (imt_hyd), IBS (ibs_hyd), OMC (omc), ISB (isb_hyd), "
                    f"JNTUH (jntuh), CBIT (cbit), GRIET (griet), VNR VJIET (vnr_vjiet), Vardhaman (vardhaman), Anurag (anurag), or IARE (iare), "
                    f"please use the 'campus_knowledge_search' tool as their data is stored in the unstructured strategic report."
                )

            filepath = hyd_dir / filename
            if not filepath.exists():
                return f"Data file not found: {filename}"

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Navigate to institution-specific key for combined files
            inst_key = INSTITUTION_KEY_MAP.get(inst_id)
            if inst_key:
                data = data.get(inst_key, data)

            formatted = self._format_topic(inst_id, data, topic_lower)
            return f"[Source: {filename}]\n{formatted}"

        except Exception as e:
            logger.error(f"InstitutionDataTool error: {e}")
            return f"Error retrieving institution data: {str(e)}"

    def _format_topic(self, inst_id: str, data: dict, topic: str) -> str:
        """Format institution data into a clean, readable response."""
        lines = []

        # ── Fees ──────────────────────────────────────────────────────────────
        if any(w in topic for w in ["fee", "cost", "tuition", "charges", "all"]):
            # IITH fees
            if "fee_structure_ug" in data:
                ug = data["fee_structure_ug"]
                lines.append("## UG Fee Structure (First Semester)")
                lines.append(f"{'Component':<40} {'General/OBC':>15} {'SC/ST/PH':>12} {'Foreign':>12}")
                lines.append("-" * 82)
                comp = ug.get("components", {})
                for name, vals in comp.items():
                    g = f"Rs {vals.get('GEN_OBC','-'):,}" if isinstance(vals.get('GEN_OBC'), int) else str(vals.get('GEN_OBC', '-'))
                    s = f"Rs {vals.get('SC_ST_PH','-'):,}" if isinstance(vals.get('SC_ST_PH'), int) else str(vals.get('SC_ST_PH', '-'))
                    fo = f"Rs {vals.get('Foreign','-'):,}" if isinstance(vals.get('Foreign'), int) else str(vals.get('Foreign', '-'))
                    lines.append(f"{name:<40} {g:>15} {s:>12} {fo:>12}")
                totals = ug.get("grand_total_first_semester", {})
                lines.append("-" * 82)
                lines.append(f"{'GRAND TOTAL (First Semester)':<40} {'Rs '+str(totals.get('GEN_OBC','?')):>15} {'Rs '+str(totals.get('SC_ST_PH','?')):>12} {'Rs '+str(totals.get('Foreign_Nationals','?')):>12}")
                lines.append("")
            if "fee_structure_pg_phd" in data:
                pg = data["fee_structure_pg_phd"]
                lines.append("## PG / PhD Fee Structure (Per Semester)")
                for prog, vals in pg.items():
                    label = prog.replace("_", " ")
                    tuition = f"Rs {vals.get('semester_tuition_fee', 0):,}"
                    ops = f"Rs {vals.get('operational_charges', 0):,}"
                    lines.append(f"  {label}: Tuition={tuition}, Ops={ops}")
                lines.append("")
            # NALSAR / NIMS fees
            if "fee_structure_first_year" in data:
                f_struct = data["fee_structure_first_year"]
                lines.append("## Fee Structure")
                lines.append(f"{'Component':<45} {'General':>12} {'SC/ST':>12}")
                lines.append("-" * 72)
                for comp, vals in f_struct.items():
                    if isinstance(vals, dict):
                        g = f"Rs {vals.get('General', '-'):,}" if isinstance(vals.get('General'), int) else str(vals.get('General', '-'))
                        s = f"Rs {vals.get('SC_ST', '-'):,}" if isinstance(vals.get('SC_ST'), int) else str(vals.get('SC_ST', '-'))
                        lines.append(f"{comp.replace('_', ' '):<45} {g:>12} {s:>12}")
                lines.append("")
            # NIMS programs with fees
            if "programs" in data:
                progs = data["programs"]
                fee_progs = [p for p in progs if p.get("fee_per_year") or p.get("fee_range") or p.get("fee")]
                if fee_progs:
                    lines.append("## Program Fee Structure")
                    lines.append(f"{'Degree':<25} {'Entrance':<12} {'Fee':<30}")
                    lines.append("-" * 70)
                    for p in fee_progs:
                        fee = (
                            f"Rs {p['fee_per_year']:,}/year" if p.get("fee_per_year")
                            else p.get("fee_range", p.get("fee", "Program-specific"))
                        )
                        lines.append(f"{p.get('degree',''):.<25} {p.get('entrance',''):.<12} {fee}")
                    lines.append("")
            # HCU hostel fees
            if "hostel_fees" in data:
                hf = data["hostel_fees"]
                lines.append("## Hostel Fee Structure")
                for cat, vals in hf.items():
                    label = cat.replace("_", " ")
                    lines.append(f"\n  Category: {label}")
                    for item, amt in vals.items():
                        lines.append(f"    {item.replace('_',' ')}: Rs {amt:,}" if isinstance(amt, int) else f"    {item}: {amt}")
                lines.append("")
            # IIITH first semester fee
            if "admissions" in data and "first_semester_tuition_fee" in data.get("admissions", {}):
                adm = data["admissions"]
                lines.append("## First Semester Fees")
                lines.append(f"  Application Fee: Rs {adm.get('application_fee', 0):,}")
                lines.append(f"  Allotment Fee (non-refundable): Rs {adm.get('allotment_fee_non_refundable', 0):,}")
                lines.append(f"  First Semester Tuition Fee: Rs {adm.get('first_semester_tuition_fee', 0):,}")
                lines.append("")

        # ── Admissions ────────────────────────────────────────────────────────
        if any(w in topic for w in ["admission", "apply", "entrance", "cutoff", "clat", "jee", "neet", "ugee", "all"]):
            if "admissions_ug" in data:
                adm = data["admissions_ug"]
                lines.append("## UG Admissions Process")
                lines.append(f"  Process: {adm.get('process', 'N/A')}")
                docs = adm.get("required_documents", [])
                if docs:
                    lines.append("  Required Documents:")
                    for d in docs:
                        lines.append(f"    • {d}")
                lines.append("")
            if "admissions" in data and "pathways" in data.get("admissions", {}):
                lines.append("## Admission Pathways")
                for path in data["admissions"]["pathways"]:
                    lines.append(f"  Channel: {path.get('channel')}")
                    lines.append(f"    Degree: {path.get('degree')}")
                    lines.append(f"    Criteria: {path.get('criteria')}")
                    if path.get("key_date_2026"):
                        lines.append(f"    Key Date 2026: {path.get('key_date_2026')}")
                lines.append("")
            if "admission" in data:
                adm = data["admission"]
                lines.append("## Admission")
                lines.append(f"  Exam: {adm.get('exam', 'N/A')}")
                lines.append(f"  Selectivity: {adm.get('selectivity', 'N/A')}")
                lines.append("")
            if "neet_cutoffs_NIMS_Hyderabad" in data:
                lines.append("## NEET Cutoff Scores (NIMS Hyderabad)")
                lines.append(f"{'Category':<30} {'2019 Score':>12} {'2020 Score':>12}")
                lines.append("-" * 56)
                for row in data["neet_cutoffs_NIMS_Hyderabad"].get("2019_vs_2020", []):
                    lines.append(f"{row.get('category',''):.<30} {str(row.get('score_2019','-')):>12} {str(row.get('score_2020','-')):>12}")
                lines.append("")

        # ── Placements ────────────────────────────────────────────────────────
        if any(w in topic for w in ["placement", "salary", "package", "lpa", "recruit", "all"]):
            placement_data = data.get("placements") or data.get("placements_2024")
            if isinstance(placement_data, dict):
                # Multi-year (IIITH format)
                if "2023" in placement_data or "2024" in placement_data:
                    lines.append("## Placement Statistics")
                    lines.append(f"{'Metric':<35} {'2023':>12} {'2024':>12} {'2025':>12}")
                    lines.append("-" * 74)
                    metrics = [
                        ("Registered Students", "registered_students"),
                        ("Placed Students", "placed_students"),
                        ("Overall Placement Rate", "placement_rate"),
                        ("Highest Salary (LPA)", "highest_salary_LPA"),
                        ("Average Salary (LPA)", "average_salary_LPA"),
                        ("Lowest Salary (LPA)", "lowest_salary_LPA"),
                    ]
                    for label, key in metrics:
                        v23 = str(placement_data.get("2023", {}).get(key, "-"))
                        v24 = str(placement_data.get("2024", {}).get(key, "-"))
                        v25 = str(placement_data.get("2025", {}).get(key, "-"))
                        lines.append(f"{label:<35} {v23:>12} {v24:>12} {v25:>12}")
                    lines.append("")
                else:
                    # IITH single-year format
                    lines.append("## Placement Statistics 2024")
                    lines.append(f"  Batch Size: {placement_data.get('batch_size', 'N/A')}")
                    lines.append(f"  Total Placements: {placement_data.get('total_placements', 'N/A')}")
                    lines.append(f"  Participating Companies: {placement_data.get('participating_companies', 'N/A')}")
                    lines.append(f"  Total Offers: {placement_data.get('total_offers', 'N/A')}")
                    lines.append(f"  International Offers: {placement_data.get('international_offers', 'N/A')}")
                    lines.append(f"  PPOs: {placement_data.get('pre_placement_offers_PPO', 'N/A')}")
                    lines.append(f"  Highest Domestic Package: Rs {placement_data.get('highest_domestic_package_LPA', 'N/A')} LPA")
                    lines.append(f"  Average Package: Rs {placement_data.get('average_package_LPA', 'N/A')} LPA")
                    med = placement_data.get("median_by_degree", {})
                    if med:
                        lines.append("  Median by Degree:")
                        for deg, pkg in med.items():
                            lines.append(f"    {deg}: {pkg}")
                    lines.append("")

        # ── Scholarships ──────────────────────────────────────────────────────
        if any(w in topic for w in ["scholarship", "financial", "aid", "waiver", "stipend", "all"]):
            sc = data.get("scholarships_financial_aid") or data.get("scholarships")
            if isinstance(sc, dict):
                lines.append("## Scholarships & Financial Aid")
                for key, val in sc.items():
                    label = key.replace("_", " ").title()
                    if isinstance(val, list):
                        lines.append(f"  {label}:")
                        for item in val:
                            if isinstance(item, dict):
                                lines.append(f"    • Income {item.get('family_income','')}: {item.get('waiver','')}")
                            else:
                                lines.append(f"    • {item}")
                    elif isinstance(val, dict):
                        lines.append(f"  {label}:")
                        lines.append(f"    Eligibility: {val.get('eligibility', 'See below')}")
                        for k, v in val.items():
                            if k != 'eligibility':
                                lines.append(f"    {k.replace('_',' ').title()}: {v}")
                    else:
                        lines.append(f"  {label}: {val}")
                lines.append("")
            elif isinstance(sc, list):
                lines.append("## Scholarships")
                for item in sc:
                    lines.append(f"  Scheme: {item.get('scheme', '')}")
                    lines.append(f"    Eligibility: {item.get('eligibility', '')}")
                    lines.append(f"    Amount: {item.get('amount', '')}")
                lines.append("")

        # ── Transport ─────────────────────────────────────────────────────────
        if any(w in topic for w in ["transport", "bus", "route", "timing", "shuttle", "all"]):
            transport = data.get("transport")
            if transport:
                lines.append("## Transport / Bus Routes")
                lines.append(f"  {transport.get('description', '')}")
                lines.append(f"  Airport Access: {transport.get('airport_access', 'N/A')}")
                for route_name, route_data in transport.get("routes", {}).items():
                    lines.append(f"\n  Route: {route_name}")
                    lines.append(f"  {'Stop':<50} {'AM Pickup':>12} {'PM Return':>12}")
                    lines.append("  " + "-" * 76)
                    for stop in route_data.get("stops", []):
                        lines.append(f"  {stop.get('stop',''):.<50} {stop.get('AM',''):>12} {stop.get('PM',''):>12}")
                lines.append("")

        # ── Hostel ────────────────────────────────────────────────────────────
        if any(w in topic for w in ["hostel", "accommodation", "room", "mess", "dining", "all"]):
            hostel = data.get("hostels_residential") or data.get("hostels")
            if hostel:
                lines.append("## Hostel & Accommodation")
                lines.append(f"  Policy: {hostel.get('policy', 'N/A')}")
                room = hostel.get("room_allocation", {})
                if room:
                    lines.append("  Room Allocation:")
                    for yr, type_ in room.items():
                        lines.append(f"    {yr.replace('_', ' ')}: {type_}")
                for block in hostel.get("hostel_blocks", []):
                    lines.append(f"    • {block.get('name','')}: {block.get('residents','')}")
                lines.append("")
            dining = data.get("dining_food")
            if dining:
                lines.append("## Dining Options")
                lines.append(f"  Booking: {dining.get('booking_system', 'N/A')}")
                for hall in dining.get("dining_halls", []):
                    lines.append(f"  • {hall.get('name','')}: {hall.get('cuisine','')}")
                lines.append("  Late Night / Commercial Outlets:")
                for outlet in dining.get("commercial_outlets", []):
                    lines.append(f"    • {outlet.get('name','')}: {outlet.get('timings','')}, {outlet.get('specialty','')}")
                lines.append("")

        # ── NIRF Rankings ─────────────────────────────────────────────────────
        if inst_id == "nirf" or any(w in topic for w in ["rank", "nirf", "all"]):
            rankings = data.get("nirf_rankings_2024", data)
            lines.append("## NIRF Rankings 2024")
            for category, entries in rankings.items():
                if isinstance(entries, list) and entries:
                    cat_name = category.replace("_", " ").title()
                    lines.append(f"\n  {cat_name}:")
                    lines.append(f"  {'Rank':<6} {'Institution':<50} {'Score/Location'}")
                    lines.append("  " + "-" * 75)
                    for e in entries:
                        score = e.get('score', '')
                        loc = e.get('location', '')
                        detail = f"{score} ({loc})" if score else loc
                        lines.append(f"  {e.get('rank','-'):<6} {e.get('institution',''):<50} {detail}")
                lines.append("")

        if not lines:
            # Return all available data formatted
            return self._dump_all(data)

        return "\n".join(lines)

    def _dump_all(self, data: dict) -> str:
        """Dump all data for an institution in a readable format."""
        def _fmt(obj, indent=0):
            lines = []
            pad = "  " * indent
            if isinstance(obj, dict):
                for k, v in obj.items():
                    label = k.replace("_", " ").title()
                    if isinstance(v, (dict, list)):
                        lines.append(f"{pad}{label}:")
                        lines.extend(_fmt(v, indent + 1))
                    else:
                        lines.append(f"{pad}{label}: {v}")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, (dict, list)):
                        lines.extend(_fmt(item, indent))
                    else:
                        lines.append(f"{pad}• {item}")
            else:
                lines.append(f"{pad}{obj}")
            return lines
        return "\n".join(_fmt(data))


# ─────────────────────────────────────────────────────────────────────────────
# Tool registry
# ─────────────────────────────────────────────────────────────────────────────

def get_all_tools() -> list:
    """Return all initialized campus tools."""
    return [
        CampusKnowledgeTool(),
        EventCalendarTool(),
        ContactDirectoryTool(),
        FacilityInfoTool(),
        ClubsActivitiesTool(),
        InstitutionDataTool(),
    ]
