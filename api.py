"""
api.py — FastAPI backend for CampusAI
Exposes chatbot, colleges, contacts, events and analytics as REST endpoints.
Run with: uvicorn api:app --reload --port 8000
"""

import os
import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

ROOT     = Path(__file__).parent
DATA_DIR = ROOT / "data"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CampusAI API",
    description="REST API for the CampusAI Universal Campus Information Chatbot",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── College registry (same as app.py) ────────────────────────────────────────
COLLEGES = [
    {"id": "general",   "name": "General (All Indian Colleges)",       "short": "General",   "icon": "🇮🇳", "type": "Universal",                        "location": "Pan-India",             "color": "#4f8ef7"},
    {"id": "iith",      "name": "IIT Hyderabad (IITH)",                "short": "IITH",      "icon": "🔬", "type": "Central Government Institute",      "location": "Kandi, Hyderabad",      "color": "#f0883e"},
    {"id": "iiith",     "name": "IIIT Hyderabad (IIITH)",              "short": "IIITH",     "icon": "💻", "type": "Autonomous Deemed University (PPP)", "location": "Gachibowli, Hyderabad", "color": "#39c5b9"},
    {"id": "nalsar",    "name": "NALSAR University of Law",            "short": "NALSAR",    "icon": "⚖️", "type": "National Law University",           "location": "Hyderabad",             "color": "#7c5cbf"},
    {"id": "nims",      "name": "NIMS — Nizam's Institute of Medical Sciences", "short": "NIMS", "icon": "🏥", "type": "Autonomous Medical University", "location": "Hyderabad",             "color": "#3fb950"},
    {"id": "hcu",       "name": "University of Hyderabad (HCU)",       "short": "HCU",       "icon": "🎓", "type": "Central University",               "location": "Gachibowli, Hyderabad", "color": "#d29922"},
    {"id": "osmania",   "name": "Osmania University",                  "short": "OU",        "icon": "📜", "type": "State University",                  "location": "Hyderabad",             "color": "#e3b341"},
    {"id": "bits_hyd",  "name": "BITS Pilani — Hyderabad Campus",      "short": "BITS Hyd",  "icon": "🏛️", "type": "Private Deemed University",        "location": "Shameerpet, Hyderabad", "color": "#58a6ff"},
    {"id": "isb_hyd",   "name": "Indian School of Business (ISB) Hyderabad", "short": "ISB Hyd", "icon": "💼", "type": "Private Business School", "location": "Gachibowli, Hyderabad", "color": "#7c5cbf"},
    {"id": "imt_hyd",   "name": "IMT Hyderabad", "short": "IMT Hyd", "icon": "📈", "type": "Private Business School", "location": "Shamshabad, Hyderabad", "color": "#f0883e"},
    {"id": "ibs_hyd",   "name": "ICFAI Business School (IBS) Hyderabad", "short": "IBS Hyd", "icon": "📊", "type": "Private Business School", "location": "Donthanapally, Hyderabad", "color": "#39c5b9"},
    {"id": "omc",       "name": "Osmania Medical College (OMC)", "short": "OMC", "icon": "🩺", "type": "Government Medical College", "location": "Koti, Hyderabad", "color": "#3fb950"},
    {"id": "nizam",     "name": "Nizam College Hyderabad", "short": "Nizam", "icon": "🏛️", "type": "Constituent College of Osmania University", "location": "Basheerbagh, Hyderabad", "color": "#d29922"},
    {"id": "st_francis","name": "St. Francis College for Women", "short": "St. Francis", "icon": "👩‍🎓", "type": "Autonomous Minority College", "location": "Begumpet, Hyderabad", "color": "#4f8ef7"},
    {"id": "jntuh",     "name": "JNTU Hyderabad (JNTUH)", "short": "JNTUH", "icon": "⚙️", "type": "State University", "location": "Kukatpally, Hyderabad", "color": "#e3b341"},
    {"id": "cbit",      "name": "Chaitanya Bharathi Institute of Technology (CBIT)", "short": "CBIT", "icon": "🏫", "type": "Autonomous Private Institute", "location": "Gandipet, Hyderabad", "color": "#4f8ef7"},
    {"id": "griet",     "name": "Gokaraju Rangaraju Institute (GRIET)", "short": "GRIET", "icon": "📐", "type": "Autonomous Private Institute", "location": "Bachupally, Hyderabad", "color": "#f0883e"},
    {"id": "vnr_vjiet", "name": "VNR VJIET", "short": "VNR VJIET", "icon": "🧪", "type": "Autonomous Private Institute", "location": "Bachupally, Hyderabad", "color": "#39c5b9"},
    {"id": "vardhaman", "name": "Vardhaman College of Engineering", "short": "Vardhaman", "icon": "🔬", "type": "Autonomous Private Institute", "location": "Shamshabad, Hyderabad", "color": "#3fb950"},
    {"id": "anurag",    "name": "Anurag University", "short": "Anurag", "icon": "🛰️", "type": "Private University", "location": "Venkatapur, Hyderabad", "color": "#7c5cbf"},
    {"id": "iare",      "name": "Institute of Aeronautical Engineering (IARE)", "short": "IARE", "icon": "✈️", "type": "Autonomous Private Institute", "location": "Dundigal, Hyderabad", "color": "#58a6ff"},
]
COLLEGE_MAP = {c["id"]: c for c in COLLEGES}

# ── Pydantic models ───────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    college_id: Optional[str] = "general"
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    tool_used: str
    response_time_ms: int
    college_id: str
    session_id: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    api_key_set: bool
    vector_store_ready: bool
    model: str
    timestamp: str

# ── Chatbot singleton ─────────────────────────────────────────────────────────
_chatbot = None

def get_chatbot():
    global _chatbot
    if _chatbot is None:
        from core.agent import CampusChatbot
        _chatbot = CampusChatbot()
    return _chatbot

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["General"])
def root():
    return {
        "name": "CampusAI API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/chat", "/colleges", "/contacts", "/events", "/analytics", "/health"]
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
def health():
    """Check system status — API key, vector store, model."""
    openai_key = os.getenv("OPENAI_API_KEY", "")
    google_key = os.getenv("GOOGLE_API_KEY", "")
    openai_ok = bool(openai_key and openai_key != "your_openai_api_key_here")
    google_ok = bool(google_key and google_key != "your_google_gemini_api_key_here")
    api_key_set = openai_ok or google_ok

    try:
        from core.embeddings import get_vector_store
        vs_ready = get_vector_store().is_ready
    except Exception:
        vs_ready = False

    provider = os.getenv("LLM_PROVIDER", "").lower().strip()
    if not provider:
        provider = "gemini" if google_ok else "openai"
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash") if provider == "gemini" else os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    return HealthResponse(
        status="ok" if api_key_set else "degraded",
        api_key_set=api_key_set,
        vector_store_ready=vs_ready,
        model=model,
        timestamp=datetime.now().isoformat(),
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(req: ChatRequest):
    """
    Send a message to CampusAI and get a response.

    - **message**: The user's question
    - **college_id**: One of: general, iith, iiith, nalsar, nims, hcu, osmania, bits_hyd, isb_hyd, imt_hyd, ibs_hyd, omc, nizam, st_francis, jntuh, cbit, griet, vnr_vjiet, vardhaman, anurag, iare
    - **session_id**: Optional session identifier for conversation history
    """
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    openai_key = os.getenv("OPENAI_API_KEY", "")
    google_key = os.getenv("GOOGLE_API_KEY", "")
    openai_ok = bool(openai_key and openai_key != "your_openai_api_key_here")
    google_ok = bool(google_key and google_key != "your_google_gemini_api_key_here")

    if not openai_ok and not google_ok:
        raise HTTPException(status_code=503, detail="API key not configured. Add GOOGLE_API_KEY or OPENAI_API_KEY to .env")

    # Build college-aware query
    college = COLLEGE_MAP.get(req.college_id or "general", {})
    if req.college_id and req.college_id != "general" and college:
        contextual = (
            f"[Context: The student is asking about {college['name']}. "
            f"Focus your answer specifically on {college['name']} when relevant data is available.]\n\n"
            f"Student question: {req.message}"
        )
    else:
        contextual = req.message

    try:
        bot = get_chatbot()
        response, tool_used, response_time_ms = bot.chat(
            contextual, session_id=req.session_id or "default"
        )
        
        # Log query to database
        try:
            from core.agent import categorize_query
            from core.database import log_query
            category = categorize_query(req.message)
            log_query(
                session_id=req.session_id or "default",
                user_query=req.message,
                bot_response=response,
                tool_used=tool_used,
                category=category,
                response_time_ms=response_time_ms
            )
        except Exception as db_err:
            logger.error(f"Failed to log API query to database: {db_err}")
            
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(
        response=response,
        tool_used=tool_used or "",
        response_time_ms=response_time_ms,
        college_id=req.college_id or "general",
        session_id=req.session_id or "default",
        timestamp=datetime.now().isoformat(),
    )



@app.get("/colleges", tags=["Data"])
def list_colleges(college_id: Optional[str] = Query(None, description="Filter by college ID")):
    """List all indexed colleges or get details for a specific one."""
    if college_id:
        college = COLLEGE_MAP.get(college_id)
        if not college:
            raise HTTPException(status_code=404, detail=f"College '{college_id}' not found")
        return college
    return {"colleges": COLLEGES, "total": len(COLLEGES)}


@app.get("/contacts", tags=["Data"])
def get_contacts(
    search: Optional[str] = Query(None, description="Search by name, dept, or designation"),
    department: Optional[str] = Query(None, description="Filter by department"),
    limit: int = Query(50, ge=1, le=200),
):
    """Search the faculty and staff contact directory."""
    try:
        contacts_file = DATA_DIR / "contacts" / "directory.csv"
        with open(contacts_file, encoding="utf-8") as f:
            contacts = list(csv.DictReader(f))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load contacts: {e}")

    if search:
        s = search.lower()
        contacts = [
            c for c in contacts
            if any(s in str(c.get(f, "")).lower()
                   for f in ["name", "designation", "department", "specialization"])
        ]
    if department:
        contacts = [c for c in contacts if c.get("department", "").lower() == department.lower()]

    return {
        "contacts": contacts[:limit],
        "total": len(contacts),
        "returned": min(len(contacts), limit),
    }


@app.get("/events", tags=["Data"])
def get_events(
    category: Optional[str] = Query(None, description="Filter by category: exam, cultural, sports, holiday, academic, placement"),
    semester: Optional[str] = Query(None, description="odd or even"),
    upcoming: bool = Query(False, description="Show only upcoming events"),
):
    """Get academic calendar events."""
    try:
        cal_file = DATA_DIR / "events" / "academic_calendar.json"
        with open(cal_file, encoding="utf-8") as f:
            data = json.load(f)

        events = []
        for sem_key in ["odd_semester", "even_semester"]:
            sem = data.get(sem_key, {})
            for ev in sem.get("events", []):
                ev["semester"] = sem.get("name", "")
                events.append(ev)

        events = sorted(events, key=lambda x: x.get("date", ""))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load events: {e}")

    today = datetime.today().date().isoformat()

    if category:
        events = [e for e in events if e.get("category", "").lower() == category.lower()]
    if semester:
        events = [e for e in events if semester.lower() in e.get("semester", "").lower()]
    if upcoming:
        events = [e for e in events if e.get("date", "") >= today]

    return {"events": events, "total": len(events)}


@app.get("/analytics", tags=["Analytics"])
def get_analytics():
    """Get chatbot usage statistics."""
    try:
        from core.database import get_analytics_summary, get_popular_queries, get_recent_queries
        summary  = get_analytics_summary()
        popular  = get_popular_queries(limit=5)
        recent   = get_recent_queries(limit=5)
        return {
            "summary": summary,
            "popular_queries": popular,
            "recent_queries": recent,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {e}")
