"""
frontend/streamlit_app.py — Streamlit UI for CampusAI
Communicates with the FastAPI backend at http://localhost:8000
Run: streamlit run frontend/streamlit_app.py
"""

import os
import sys
import json
import logging
import time
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Optional

import streamlit as st
import httpx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="CampusAI — Universal Campus Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
def load_css():
    css_path = ROOT / "ui" / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    dark = st.session_state.get("dark_mode", False)
    if dark:
        st.markdown("""<style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"],
        [data-testid="stAppViewContainer"] > div, .main, .block-container {
          background-color: #04080f !important; color: #f0f4ff !important; }
        .campus-header { background: linear-gradient(135deg,rgba(99,102,241,0.1),rgba(139,92,246,0.08)) !important; border:1px solid rgba(99,102,241,0.18) !important; }
        .college-card, .metric-card, .info-card, .contact-card { background: linear-gradient(145deg,#0d1e35,#060d1a) !important; border-color:rgba(99,102,241,0.12) !important; }
        .college-card-name, .info-card-title, .contact-name { color: #f0f4ff !important; }
        .college-card-desc, .info-card-desc, .contact-dept, .contact-info { color: #8ba3c7 !important; }
        .message.bot .message-bubble { background: linear-gradient(145deg,#0d1e35,#080f1e) !important; border-color:rgba(99,102,241,0.15) !important; color:#f0f4ff !important; }
        [data-testid="stTextInput"] input { background-color:#0d1e35 !important; border-color:rgba(99,102,241,0.2) !important; color:#f0f4ff !important; }
        [data-testid="stTabs"] [data-baseweb="tab-list"] { background:#0d1e35 !important; }
        [data-testid="stExpander"] { background-color:#0d1e35 !important; }
        hr { background: linear-gradient(90deg,transparent,rgba(99,102,241,0.2),transparent) !important; }
        .badge-exam{background:rgba(245,158,11,0.12)!important;color:#fbbf24!important}
        .badge-cultural{background:rgba(139,92,246,0.12)!important;color:#a78bfa!important}
        .badge-sports{background:rgba(16,185,129,0.1)!important;color:#34d399!important}
        .badge-holiday{background:rgba(6,182,212,0.1)!important;color:#22d3ee!important}
        .badge-academic{background:rgba(99,102,241,0.12)!important;color:#818cf8!important}
        .badge-placement{background:rgba(244,63,94,0.1)!important;color:#fb7185!important}
        </style>""", unsafe_allow_html=True)
    else:
        st.markdown("""<style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"],
        [data-testid="stAppViewContainer"] > div, .main, .block-container {
          background-color: #f0f4ff !important; color: #0f172a !important; }
        .campus-header { background:#ffffff !important; border:1px solid rgba(99,102,241,0.1) !important; }
        .college-card, .metric-card, .info-card, .contact-card { background:#ffffff !important; border-color:#e2e8f0 !important; }
        .message.bot .message-bubble { background:#ffffff !important; border-color:#e2e8f0 !important; color:#0f172a !important; }
        [data-testid="stTextInput"] input,
        [data-testid="stTextInput"] > div > div > input,
        .stTextInput input { background-color:#ffffff !important; border-color:#e2e8f0 !important; color:#0f172a !important; }
        [data-testid="stTextInput"] > div > div { background-color:#ffffff !important; }
        [data-testid="stTextInput"] input::placeholder { color:#94a3b8 !important; }
        [data-testid="stTabs"] [data-baseweb="tab-list"] { background:#ffffff !important; }
        [data-testid="stExpander"] { background-color:#ffffff !important; }
        [data-testid="stSelectbox"] > div { background-color:#ffffff !important; border-color:#e2e8f0 !important; color:#0f172a !important; }
        [data-baseweb="input"] { background-color:#ffffff !important; }
        [data-baseweb="base-input"] { background-color:#ffffff !important; color:#0f172a !important; }
        .badge-exam{background:#fef3c7!important;color:#92400e!important}
        .badge-cultural{background:#ede9fe!important;color:#5b21b6!important}
        .badge-sports{background:#dcfce7!important;color:#14532d!important}
        .badge-holiday{background:#cffafe!important;color:#164e63!important}
        .badge-academic{background:#e0e7ff!important;color:#3730a3!important}
        .badge-placement{background:#ffe4e6!important;color:#9f1239!important}
        </style>""", unsafe_allow_html=True)

# ── API helpers ───────────────────────────────────────────────────────────────
def api_get(path: str, params: dict = None):
    try:
        r = httpx.get(f"{API_BASE}{path}", params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except httpx.ConnectError:
        st.error("⚠️ Cannot connect to backend. Make sure the FastAPI server is running: `uvicorn backend.main:app --reload --port 8000`")
        return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None

def api_post(path: str, body: dict):
    try:
        r = httpx.post(f"{API_BASE}{path}", json=body, timeout=60)
        r.raise_for_status()
        return r.json()
    except httpx.ConnectError:
        st.error("⚠️ Cannot connect to backend. Make sure the FastAPI server is running.")
        return None
    except Exception as e:
        logger.error(f"API POST error: {e}")
        return None

# ── Session state ─────────────────────────────────────────────────────────────
def init_session_state():
    defaults = {
        "messages": [],
        "session_id": str(uuid.uuid4()),
        "page": "💬 Chat",
        "feedback_given": set(),
        "selected_college": None,
        "dark_mode": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()
load_css()

# ── College registry (local copy for UI) ─────────────────────────────────────
data = api_get("/colleges")
COLLEGES = data["colleges"] if data else []
COLLEGE_MAP = {c["id"]: c for c in COLLEGES}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    is_dark = st.session_state.dark_mode
    if st.button("☀️ Light Mode" if is_dark else "🌙 Dark Mode", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🎓</div>
        <div class="sidebar-brand-name">CampusAI</div>
        <div class="sidebar-brand-sub">Universal Campus Guide</div>
    </div>
    """, unsafe_allow_html=True)

    active_college = st.session_state.get("selected_college")
    if active_college:
        c_info = COLLEGE_MAP.get(active_college, {})
        badge_color = c_info.get("color", "#6366f1")
        st.markdown(f"""
        <div class="college-badge">
            <div style="font-size:2rem;margin-bottom:0.3rem">{c_info.get('icon','🏫')}</div>
            <div style="font-size:0.8rem;font-weight:700;color:#f1f5f9">{c_info.get('short','—')}</div>
            <div style="font-size:0.65rem;color:#64748b;margin-top:0.1rem">{c_info.get('type','')}</div>
            <div style="width:40px;height:2px;background:{badge_color};border-radius:1px;margin:0.5rem auto 0"></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Switch College", use_container_width=True):
            st.session_state.selected_college = None
            st.session_state.messages = []
            st.session_state.feedback_given = set()
            st.rerun()
        st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    pages = ["💬 Chat", "📊 Dashboard", "📅 Events", "📞 Contacts", "📈 Analytics"]
    selected_page = st.radio("Navigate", pages, index=pages.index(st.session_state.page), label_visibility="collapsed")
    st.session_state.page = selected_page

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)

    # Backend health
    health = api_get("/health")
    api_ok = health.get("api_key_set", False) if health else False
    vs_ready = health.get("vector_store_ready", False) if health else False
    model = health.get("model", "gemini-2.0-flash") if health else "unknown"

    st.markdown(f"""
    <div style="padding:0 0.25rem">
        <div style="font-size:0.62rem;font-weight:700;color:rgba(255,255,255,0.3);
                    text-transform:uppercase;letter-spacing:0.14em;margin-bottom:0.5rem">System Status</div>
        <div class="stat-row">
            <span class="stat-label">🧠 Gemini AI</span>
            <span class="stat-value" style="color:{'#4ade80' if api_ok else '#f87171'}">{'● Online' if api_ok else '● Offline'}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">📚 Knowledge</span>
            <span class="stat-value" style="color:{'#4ade80' if vs_ready else '#fbbf24'}">{'433 chunks' if vs_ready else '● Empty'}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">🏛️ Colleges</span>
            <span class="stat-value">{len(COLLEGES)} indexed</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">🤖 Model</span>
            <span class="stat-value" style="font-size:0.62rem">{model}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">⚡ Backend</span>
            <span class="stat-value" style="color:{'#4ade80' if health else '#f87171'}">{'● Connected' if health else '● Offline'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)

    msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    if msg_count > 0:
        st.caption(f"💬 {msg_count} message{'s' if msg_count != 1 else ''} this session")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.feedback_given = set()
        st.rerun()

# ── College Selection Screen ──────────────────────────────────────────────────
if st.session_state.get("selected_college") is None:

    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem 0.5rem;position:relative">
        <div style="position:relative;display:inline-block;margin-bottom:1.5rem">
            <div style="font-size:5rem;display:inline-block;
                        animation:floatIcon 3s ease-in-out infinite;
                        filter:drop-shadow(0 8px 24px rgba(99,102,241,0.35))">🎓</div>
        </div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:2.8rem;font-weight:900;
                    background:linear-gradient(135deg,#6366f1,#8b5cf6,#06b6d4);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;letter-spacing:-0.04em;line-height:1.05;
                    margin-bottom:0.5rem;background-size:200%;animation:gradShift 5s linear infinite">
            Welcome to CampusAI
        </div>
        <div style="font-size:1rem;color:#475569;max-width:480px;margin:0 auto;line-height:1.7">
            Your AI-powered guide for Indian colleges —
            <span style="color:#6366f1;font-weight:600">choose your institution</span> to begin.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    for row_start in range(0, len(COLLEGES), 4):
        row_colleges = COLLEGES[row_start:row_start + 4]
        cols = st.columns(len(row_colleges), gap="small")
        for col, c in zip(cols, row_colleges):
            with col:
                tags_html = " ".join(f'<span class="college-tag">{t}</span>' for t in c.get("tags", []))
                st.markdown(f"""
                <div class="college-card" style="--card-gradient:linear-gradient(90deg,{c['color']},{c['color']}80)">
                    <div class="college-card-header">
                        <div class="college-card-icon">{c['icon']}</div>
                        <div>
                            <div class="college-card-name">{c['name']}</div>
                            <div class="college-card-type">{c['type']}</div>
                        </div>
                    </div>
                    <div class="college-card-desc">{c.get('desc','')}</div>
                    <div class="college-card-tags">{tags_html}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"{c['icon']} Select {c['short']}", key=f"select_{c['id']}", use_container_width=True):
                    st.session_state.selected_college = c["id"]
                    st.session_state.messages = []
                    st.session_state.page = "💬 Chat"
                    st.rerun()

    st.stop()

# ── Chat page ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "💬 Chat":
    active_c = COLLEGE_MAP.get(st.session_state.selected_college, {})

    st.markdown(f"""
    <div class="campus-header">
        <h1>{active_c.get('icon','🎓')} {active_c.get('name','CampusAI')}</h1>
        <p>Ask me anything — fees, admissions, placements, facilities, clubs &amp; more.</p>
        <div style="display:flex;gap:0.6rem;margin-top:0.8rem;flex-wrap:wrap">
            <span style="background:#eef2ff;border:1.5px solid #c7d2fe;border-radius:20px;padding:0.2rem 0.8rem;font-size:0.72rem;color:#4f46e5;font-weight:600">🤖 Gemini 1.5 Flash</span>
            <span style="background:#f0fdf4;border:1.5px solid #bbf7d0;border-radius:20px;padding:0.2rem 0.8rem;font-size:0.72rem;color:#15803d;font-weight:600">📚 389 Knowledge Docs</span>
            <span style="background:#ecfeff;border:1.5px solid #a5f3fc;border-radius:20px;padding:0.2rem 0.8rem;font-size:0.72rem;color:#0e7490;font-weight:600">⚡ FastAPI Backend</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion chips
    college_suggestions = {
        "general":  ["📚 Library timings", "🏠 Hostel rules", "📝 Bonafide certificate", "📅 Cultural fest dates", "💼 Placement tips", "🎓 CGPA calculation", "🔬 Technical clubs", "📋 Admission documents"],
        "iith":     ["📐 Fractal Academics model", "💰 IITH fee structure", "🚌 Bus timing from Nagole", "🎓 MCM scholarship", "💼 IITH placements 2024", "📋 JoSAA counseling docs", "🚌 Bus from Miyapur", "💰 SC/ST tuition waiver"],
        "iiith":    ["💻 Ada cluster specs", "🍽️ Kadamba dining menu", "🏠 Hostel allocation policy", "💼 IIITH placements 2025", "📝 UGEE exam details", "🌙 Night canteen options", "💰 First semester fee", "📡 PGEE admission"],
        "nalsar":   ["📋 CLAT cutoff rank", "💰 NALSAR fee structure", "🎓 Ishan Uday scholarship", "👩 Indira Gandhi scholarship", "📝 Admission process", "⚖️ LLB programs offered", "💰 SC/ST fee concession", "🏛️ Law school facilities"],
        "nims":     ["🩺 NEET PG cutoff by category", "📋 MD/MS admission", "💰 DNB program fee", "🏥 BPT eligibility", "📝 NIMSET exam pattern", "🩺 DM specialty programs", "💰 Nursing program fee", "📋 MHM admission"],
        "hcu":      ["🏠 50 km hostel rule", "📱 Samarth portal process", "💰 Hostel fee SC/ST", "📝 GRE requirements", "🌐 IELTS score needed", "🏠 Hostel allotment rules", "⏰ 48-hour occupancy rule", "💰 Room rent waiver"],
        "osmania":  ["📊 SGPA CGPA formula", "📝 Internal exam format", "✅ Attendance requirement", "📋 CBCS credit system", "🎓 Semester structure", "📊 Internal marks breakdown", "📝 MCQ test pattern", "🎓 End semester exam"],
        "bits_hyd": ["🛒 Campus shops list", "🏥 Medical center timings", "🏦 SBI branch on campus", "🛒 MORE supermarket", "🍞 Bakery on campus", "📬 Post office facilities", "💊 Pharmacy details", "🏥 Medicity hospital tie-up"],
    }
    suggestions = college_suggestions.get(st.session_state.selected_college, college_suggestions["general"])
    cols = st.columns(4)
    for i, sug in enumerate(suggestions):
        if cols[i % 4].button(sug, key=f"sug_{i}", use_container_width=True):
            text = sug.split(" ", 1)[1] if " " in sug else sug
            _r = api_post("/chat", {"message": text, "college_id": st.session_state.selected_college, "session_id": st.session_state.session_id})
            if _r:
                ts = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({"role": "user", "content": text, "timestamp": ts})
                st.session_state.messages.append({"role": "assistant", "content": _r["response"], "timestamp": ts, "tool_used": _r.get("tool_used", "")})
            st.rerun()

    st.divider()

    if not st.session_state.messages:
        st.markdown(f"""
        <div class="empty-state">
            <span class="empty-state-icon">{active_c.get('icon','👋')}</span>
            <div class="empty-state-title">Ready to help with {active_c.get('short','your college')}!</div>
            <div class="empty-state-desc">Ask about fees, placements, admissions, hostel rules, scholarships, clubs, or anything else.</div>
        </div>
        """, unsafe_allow_html=True)

    for idx, msg in enumerate(st.session_state.messages):
        role = msg["role"]
        content = msg["content"]
        ts = msg.get("timestamp", "")
        tool = msg.get("tool_used", "")

        if role == "user":
            st.markdown(f"""
            <div class="message user">
                <div class="message-avatar">👤</div>
                <div><div class="message-bubble">{content}</div>
                <div class="message-meta" style="text-align:right">{ts}</div></div>
            </div>""", unsafe_allow_html=True)
        else:
            tool_badge = f'<span class="event-badge badge-academic" style="margin-left:0.5rem">{tool}</span>' if tool else ""
            st.markdown(f"""
            <div class="message bot">
                <div class="message-avatar">🎓</div>
                <div style="width:100%">
                    <div class="message-bubble">{content}</div>
                    <div class="message-meta">{ts} {tool_badge}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.divider()

    col_input, col_send = st.columns([6, 1])
    with col_input:
        user_input = st.text_input("Message", placeholder="Ask anything about campus life...", label_visibility="collapsed", key="chat_input")
    with col_send:
        send_btn = st.button("Send 🚀", use_container_width=True)

    if send_btn and user_input:
        ts = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": ts})
        with st.spinner(""):
            resp = api_post("/chat", {"message": user_input, "college_id": st.session_state.selected_college, "session_id": st.session_state.session_id})
        if resp:
            st.session_state.messages.append({"role": "assistant", "content": resp["response"], "timestamp": datetime.now().strftime("%H:%M"), "tool_used": resp.get("tool_used", "")})
        st.rerun()

# ── Dashboard ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "📊 Dashboard":
    st.markdown('<div class="campus-header"><h1>📊 Campus Intelligence Dashboard</h1><p>Overview of campus information categories and quick access resources.</p></div>', unsafe_allow_html=True)

    analytics = api_get("/analytics")
    stats = analytics.get("summary", {}) if analytics else {}

    m1, m2, m3, m4 = st.columns(4)
    for col, val, label, icon in [
        (m1, stats.get("total_queries", 0), "Total Queries", "💬"),
        (m2, stats.get("today_queries", 0), "Today's Queries", "📅"),
        (m3, f"{stats.get('satisfaction_rate', 0)}%", "Satisfaction", "⭐"),
        (m4, f"{int(stats.get('avg_response_time_ms', 0))}ms", "Avg Response", "⚡"),
    ]:
        col.markdown(f'<div class="metric-card"><div style="font-size:1.5rem">{icon}</div><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

# ── Events ────────────────────────────────────────────────────────────────────
elif st.session_state.page == "📅 Events":
    st.markdown('<div class="campus-header"><h1>📅 Academic Calendar & Events</h1><p>Complete academic year schedule — exams, fests, sports, holidays, and important deadlines.</p></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        category_filter = st.selectbox("Category", ["All", "Exam", "Cultural", "Technical", "Sports", "Holiday", "Academic", "Placement"])
    with col2:
        semester_filter = st.selectbox("Semester", ["All Semesters", "Odd Semester", "Even Semester"])
    with col3:
        show_upcoming = st.checkbox("Upcoming Only", value=False)

    params = {}
    if category_filter != "All":
        params["category"] = category_filter.lower()
    if semester_filter != "All Semesters":
        params["semester"] = "odd" if "Odd" in semester_filter else "even"
    if show_upcoming:
        params["upcoming"] = True

    data = api_get("/events", params=params)
    events = data.get("events", []) if data else []
    st.caption(f"Showing {len(events)} events")
    st.divider()

    badge_map = {"exam": "badge-exam", "cultural": "badge-cultural", "sports": "badge-sports", "holiday": "badge-holiday", "academic": "badge-academic", "placement": "badge-placement"}
    today_str = date.today().isoformat()
    grouped = {}
    for ev in events:
        d = ev.get("date", "")
        month = datetime.strptime(d[:7], "%Y-%m").strftime("%B %Y") if len(d) >= 7 else "TBA"
        grouped.setdefault(month, []).append(ev)

    for month, evs in grouped.items():
        st.markdown(f"**📆 {month}**")
        for ev in evs:
            cat = ev.get("category", "academic").lower()
            badge = badge_map.get(cat, "badge-academic")
            is_past = ev.get("date", "") < today_str
            st.markdown(f"""
            <div class="contact-card" style="margin-bottom:0.5rem;opacity:{'0.5' if is_past else '1'}">
                <div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap">
                    <div style="font-weight:600;color:#0f172a">{ev.get('event','')}</div>
                    <span class="event-badge {badge}">{cat}</span>
                    {'<span class="event-badge" style="background:#f1f5f9;color:#94a3b8">Past</span>' if is_past else ''}
                </div>
                <div style="font-size:0.8rem;color:#94a3b8;margin-top:0.3rem">📅 {ev.get('date','TBA')}</div>
                <div style="font-size:0.85rem;color:#475569;margin-top:0.4rem">{ev.get('description','')}</div>
            </div>""", unsafe_allow_html=True)

# ── Contacts ──────────────────────────────────────────────────────────────────
elif st.session_state.page == "📞 Contacts":
    st.markdown('<div class="campus-header"><h1>📞 Faculty & Staff Directory</h1><p>Search for any faculty, HOD, warden, or administrative contact.</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        search_term = st.text_input("Search", placeholder="🔍 Search by name, department, designation...", label_visibility="collapsed")
    with col2:
        dept_filter = st.text_input("Department", placeholder="Filter by department...", label_visibility="collapsed")

    params = {"limit": 100}
    if search_term:
        params["search"] = search_term
    if dept_filter:
        params["department"] = dept_filter

    data = api_get("/contacts", params=params)
    contacts = data.get("contacts", []) if data else []
    st.caption(f"Found {data.get('total', 0) if data else 0} contacts")
    st.divider()

    cols = st.columns(2)
    for i, c in enumerate(contacts):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="contact-card" style="margin-bottom:1rem">
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;box-shadow:0 4px 16px rgba(99,102,241,0.3)">👤</div>
                    <div>
                        <div class="contact-name">{c.get('name','N/A')}</div>
                        <div class="contact-role">{c.get('designation','')}</div>
                        <div class="contact-dept">{c.get('department','')}</div>
                    </div>
                </div>
                <div style="height:1px;background:rgba(0,0,0,0.06);margin:0.75rem 0"></div>
                <div class="contact-info">
                    📧 <a href="mailto:{c.get('email','')}" style="color:#6366f1;text-decoration:none">{c.get('email','N/A')}</a><br>
                    📞 {c.get('phone','N/A')}<br>
                    🏢 {c.get('office_location','N/A')}<br>
                    🕐 {c.get('office_hours','N/A')}
                </div>
            </div>""", unsafe_allow_html=True)

# ── Analytics ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "📈 Analytics":
    st.markdown('<div class="campus-header"><h1>📈 Chatbot Analytics</h1><p>Usage statistics and performance metrics.</p></div>', unsafe_allow_html=True)

    data = api_get("/analytics")
    if not data:
        st.stop()

    stats = data.get("summary", {})
    c1, c2, c3, c4, c5 = st.columns(5)
    for col, val, label, icon in [
        (c1, stats.get("total_queries", 0),       "Total Queries", "💬"),
        (c2, stats.get("today_queries", 0),        "Today",         "📅"),
        (c3, stats.get("positive_feedback", 0),   "👍 Helpful",    "✅"),
        (c4, stats.get("negative_feedback", 0),   "👎 Not Helpful","❌"),
        (c5, f"{stats.get('satisfaction_rate',0)}%","Satisfaction", "⭐"),
    ]:
        col.markdown(f'<div class="metric-card"><div style="font-size:1.2rem">{icon}</div><div class="metric-value" style="font-size:1.5rem">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-title">📅 Queries Per Day</div>', unsafe_allow_html=True)
        daily = stats.get("daily_counts", [])
        if daily:
            fig = px.bar(pd.DataFrame(daily), x="day", y="count", color_discrete_sequence=["#6366f1"], template="plotly_white")
            fig.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#f0f4ff", margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title">🏷️ Queries by Category</div>', unsafe_allow_html=True)
        top_cats = stats.get("top_categories", [])
        if top_cats:
            fig2 = px.pie(pd.DataFrame(top_cats), names="category", values="count", color_discrete_sequence=["#6366f1","#8b5cf6","#06b6d4","#10b981","#f59e0b"], template="plotly_white", hole=0.45)
            fig2.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#f0f4ff", margin=dict(l=10,r=10,t=10,b=10))
            st.plotly_chart(fig2, use_container_width=True)

    avg_rt = stats.get("avg_response_time_ms", 0)
    st.markdown(f"""
    <div style="text-align:center;padding:1rem 1.5rem;color:#475569;font-size:0.85rem;background:#ffffff;border:1.5px solid #e2e8f0;border-radius:16px">
        ⚡ Avg Response: <strong style="color:#6366f1">{int(avg_rt)}ms</strong> &nbsp;·&nbsp;
        ⚡ Backend: <strong style="color:#10b981">{API_BASE}</strong>
    </div>
    """, unsafe_allow_html=True)
