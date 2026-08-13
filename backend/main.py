"""
backend/main.py — FastAPI backend for CampusAI (CANONICAL)
This is the primary backend. Run: uvicorn backend.main:app --reload --port 8000
"""

import os
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# ── Shared config (single source of truth) ────────────────────────────────────
from core.config import COLLEGES, COLLEGE_MAP, DATA_DIR
from core.data_loader import load_contacts, load_events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CampusAI API",
    description="REST API for the CampusAI Universal Campus Information Chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Chatbot singleton ─────────────────────────────────────────────────────────
_chatbot = None

def get_chatbot():
    global _chatbot
    if _chatbot is None:
        from core.agent import CampusChatbot
        _chatbot = CampusChatbot()
    return _chatbot

# ── Pydantic schemas ──────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    college_id: Optional[str] = "general"
    session_id: Optional[str] = "default"

    model_config = {"json_schema_extra": {"example": {
        "message": "What is the CGPA calculation formula?",
        "college_id": "osmania",
        "session_id": "user_123"
    }}}

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

class FeedbackRequest(BaseModel):
    message_id: Optional[str] = None
    rating: int
    session_id: Optional[str] = "default"
    feedback_text: Optional[str] = ""

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["General"])
def root():
    """API root — lists all available endpoints."""
    return {
        "name": "CampusAI API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "POST /chat":       "Send a message and get a chatbot response",
            "GET  /colleges":   "List all indexed colleges",
            "GET  /contacts":   "Search faculty & staff directory",
            "GET  /events":     "Academic calendar and events",
            "GET  /analytics":  "Usage statistics",
            "GET  /health":     "System health check",
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
def health():
    """System health — API key status, vector store, model name."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    api_key_set = bool(api_key and api_key != "your_openai_api_key_here")

    try:
        from core.embeddings import get_vector_store
        vs_ready = get_vector_store().is_ready
    except Exception:
        vs_ready = False

    return HealthResponse(
        status="ok" if api_key_set else "degraded",
        api_key_set=api_key_set,
        vector_store_ready=vs_ready,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        timestamp=datetime.now().isoformat(),
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(req: ChatRequest):
    """
    Send a message to CampusAI.

    - **message**: The student's question
    - **college_id**: Target college (general, iith, iiith, nalsar, nims, hcu, osmania, bits_hyd, isb_hyd, imt_hyd, ibs_hyd, omc, nizam, st_francis, jntuh, cbit, griet, vnr_vjiet, vardhaman, anurag, iare)
    - **session_id**: Session ID for conversation continuity
    """
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key == "your_openai_api_key_here":
        raise HTTPException(status_code=503, detail="API key not configured. Add OPENAI_API_KEY to .env")

    college = COLLEGE_MAP.get(req.college_id or "general", {})
    if req.college_id and req.college_id != "general" and college:
        contextual = (
            f"[Context: Student is asking about {college['name']}. "
            f"Focus on {college['name']} when relevant data is available.]\n\n"
            f"Student question: {req.message}"
        )
    else:
        contextual = req.message

    try:
        bot = get_chatbot()
        response, tool_used, response_time_ms = bot.chat(
            contextual, session_id=req.session_id or "default"
        )
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
def list_colleges(college_id: Optional[str] = Query(None, description="Specific college ID")):
    """List all colleges or get one by ID."""
    if college_id:
        college = COLLEGE_MAP.get(college_id)
        if not college:
            raise HTTPException(status_code=404, detail=f"College '{college_id}' not found. Valid IDs: {list(COLLEGE_MAP.keys())}")
        return college
    return {"colleges": COLLEGES, "total": len(COLLEGES)}


@app.get("/contacts", tags=["Data"])
def get_contacts(
    search: Optional[str] = Query(None, description="Search by name, dept or designation"),
    department: Optional[str] = Query(None, description="Filter by department name"),
    limit: int = Query(50, ge=1, le=200, description="Max results to return"),
):
    """Search the faculty and staff contact directory."""
    contacts = load_contacts()
    if not contacts:
        raise HTTPException(status_code=500, detail="Could not load contacts")

    if search:
        s = search.lower()
        contacts = [c for c in contacts if any(
            s in str(c.get(f, "")).lower()
            for f in ["name", "designation", "department", "specialization"]
        )]
    if department:
        contacts = [c for c in contacts if c.get("department", "").lower() == department.lower()]

    return {"contacts": contacts[:limit], "total": len(contacts), "returned": min(len(contacts), limit)}


@app.get("/events", tags=["Data"])
def get_events(
    category: Optional[str] = Query(None, description="exam | cultural | sports | holiday | academic | placement"),
    semester: Optional[str] = Query(None, description="odd | even"),
    upcoming: bool = Query(False, description="Only show upcoming events"),
):
    """Get academic calendar events with optional filters."""
    events = load_events()
    if not events:
        raise HTTPException(status_code=500, detail="Could not load events")

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
    """Chatbot usage statistics and popular queries."""
    try:
        from core.database import get_analytics_summary, get_popular_queries, get_recent_queries
        return {
            "summary": get_analytics_summary(),
            "popular_queries": get_popular_queries(limit=5),
            "recent_queries": get_recent_queries(limit=5),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {e}")


@app.post("/feedback", tags=["Analytics"])
def submit_feedback(req: FeedbackRequest):
    """Log thumbs up/down feedback for the latest query in a session."""
    if req.rating not in (1, -1):
        raise HTTPException(status_code=422, detail="rating must be 1 (up) or -1 (down)")

    from core.database import get_connection, log_feedback
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM query_history WHERE session_id = ? ORDER BY timestamp DESC LIMIT 1",
        (req.session_id or "default",),
    )
    row = cursor.fetchone()
    conn.close()

    query_id = dict(row)["id"] if row else None
    if query_id is not None:
        log_feedback(query_id, req.rating, req.feedback_text or "")

    return {"status": "ok", "logged": query_id is not None, "query_id": query_id}
