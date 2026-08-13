"""
app.py — Main Streamlit entry point for CampusAI.
Delegates all page rendering to pages/ modules.
"""

import os
import sys
import logging
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# ── Load .env (cloud-aware) ───────────────────────────────────────────────────
load_dotenv(ROOT / ".env")

try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except Exception as e:
    logging.getLogger(__name__).debug(f"Streamlit secrets not available: {e}")

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# ── Page Config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="CampusAI \u2014 Universal Campus Assistant",
    page_icon="\U0001f3eb",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/campus-ai",
        "About": "CampusAI \u2014 Universal Campus Information Assistant for Indian Colleges",
    },
)

# ── Session State Initialization ──────────────────────────────────────────────
def _init_session_state():
    defaults = {
        "messages": [],
        "session_id": str(uuid.uuid4()),
        "chatbot": None,
        "db_initialized": False,
        "vs_loaded": False,
        "page": "\U0001f3e0 Overview",
        "feedback_given": set(),
        "contact_filter": "",
        "event_filter": "all",
        "selected_college": None,
        "dark_mode": False,
        "last_selected_college": None,
        "last_page": "\U0001f3e0 Overview",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


_init_session_state()

# Force light mode as default (overwrite stale dark_mode=True from old sessions)
if st.session_state.get("dark_mode", False) is True and "dark_mode_v2" not in st.session_state:
    st.session_state.dark_mode = False
    st.session_state.dark_mode_v2 = True

# ── Load Theme ────────────────────────────────────────────────────────────────
from ui.theme import load_css
from core.config import COLLEGE_MAP

load_css(selected_college=st.session_state.get("selected_college"))

# ── Database Initialization ───────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def _get_database():
    from core.database import initialize_database
    initialize_database()
    return True

try:
    _get_database()
    st.session_state.db_initialized = True
except Exception as e:
    logging.getLogger(__name__).error(f"DB init failed: {e}")

# ── Sidebar ───────────────────────────────────────────────────────────────────
from core.config import is_openai_configured, is_google_configured, get_active_provider
from ui.components import get_college_logo_html

with st.sidebar:
    # Theme toggle
    is_dark = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    if is_dark != st.session_state.dark_mode:
        st.session_state.dark_mode = is_dark
        st.rerun()
    st.markdown("<div style='margin-bottom:0.75rem'></div>", unsafe_allow_html=True)

    # Brand
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.85rem; padding:1.1rem 0 1.4rem 0; border-bottom:1px solid var(--border); margin-bottom:1.5rem;">
        <div style="width:44px; height:44px; background:linear-gradient(135deg,#0052FF,#4D7CFF); border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0; box-shadow:0 4px 12px rgba(0,82,255,0.28);">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 3L22 8.5L12 14L2 8.5L12 3Z" stroke="white" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>
                <path d="M6 11V16.5C8.5 18.8 15.5 18.8 18 16.5V11" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="22" y1="8.5" x2="22" y2="13" stroke="white" stroke-width="1.6" stroke-linecap="round"/>
                <circle cx="22" cy="14" r="1.1" fill="white"/>
            </svg>
        </div>
        <div>
            <div style="font-family:'Calistoga',Georgia,serif; font-size:1.22rem; font-weight:400; color:var(--text-primary); letter-spacing:-0.01em; line-height:1.2;">CampusAI</div>
            <div style="font-size:0.62rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.08em; font-weight:600; margin-top:0.15rem; font-family:'Inter',sans-serif;">College Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active college badge
    active_college = st.session_state.get("selected_college")
    if active_college:
        c_info = COLLEGE_MAP.get(active_college, {})
        st.markdown(f"""
        <div class="college-badge" style="display:flex; flex-direction:column; align-items:center; text-align:center; padding:1.25rem;">
            <div style="margin-bottom:0.5rem">{get_college_logo_html(active_college, size=40)}</div>
            <div style="font-size:1.0rem;font-weight:600;color:var(--text-primary);letter-spacing:-0.01em;margin-top:0.25rem">{c_info.get('short','\u2014')}</div>
            <div style="font-size:0.65rem;color:var(--text-secondary);margin-top:0.1rem">{c_info.get('type','')}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("\U0001f504 Switch College", use_container_width=True):
            st.session_state.selected_college = None
            st.session_state.messages = []
            st.session_state.feedback_given = set()
            st.session_state.page = "\U0001f3e0 Overview"
            if st.session_state.get("chatbot") is not None:
                st.session_state.chatbot.clear_history(st.session_state.session_id)
                st.session_state.chatbot = None
            st.rerun()
        st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    # Navigation
    pages = [
        "\U0001f3e0 Overview", "\U0001f4ac Chat", "\u2696\ufe0f Compare",
        "\U0001f4ca Dashboard", "\U0001f4c5 Events", "\U0001f4de Contacts", "\U0001f4c8 Insights",
    ]
    _page_labels = {
        "\U0001f3e0 Overview": "Overview", "\U0001f4ac Chat": "Chat",
        "\u2696\ufe0f Compare": "Compare", "\U0001f4ca Dashboard": "Dashboard",
        "\U0001f4c5 Events": "Events", "\U0001f4de Contacts": "Contacts",
        "\U0001f4c8 Insights": "Insights",
    }
    selected_page = st.radio(
        "Navigate", pages,
        index=pages.index(st.session_state.page) if st.session_state.page in pages else 0,
        label_visibility="collapsed",
        format_func=lambda x: _page_labels.get(x, x),
    )
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)

    # System status
    openai_ok = is_openai_configured()
    google_ok = is_google_configured()
    provider = get_active_provider()
    api_ok = openai_ok or google_ok

    try:
        from core.embeddings import get_vector_store
        vs_ready = get_vector_store().is_ready
    except Exception:
        vs_ready = False

    status_color = "#10b981" if api_ok else "#ef4444"
    if provider == "gemini" and google_ok:
        status_text = "Gemini Online"
    elif openai_ok:
        status_text = "OpenAI Online"
    else:
        status_text = "System Offline"
    status_emoji = "\U0001f7e2" if api_ok else "\U0001f534"

    # Vector store doc count
    try:
        from core.embeddings import get_vector_store
        vs = get_vector_store()
        doc_count = len(vs.documents) if vs.is_ready else 0
    except Exception:
        doc_count = 0

    from core.config import COLLEGES as _COLLEGES

    st.markdown(f"""
    <div style="padding:0 0.25rem">
        <div style="font-size:0.65rem;font-weight:700;color:var(--text-secondary);
                    text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.75rem;
                    font-family:'JetBrains Mono',monospace">System Status</div>
        <div style="display:flex;flex-direction:column;gap:0.6rem;font-size:0.88rem;color:var(--text-primary);padding-left:0.2rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span style="color:{status_color};font-size:0.8rem;">{status_emoji}</span>
                <span>{status_text}</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span>\U0001f4da</span>
                <span>{doc_count} Chunks</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span>\U0001f3eb</span>
                <span>{len(_COLLEGES)} Colleges</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)

    with st.expander("\U0001f3eb Indexed Colleges", expanded=False):
        from core.config import INDEXED_COLLEGE_IDS
        for c in _COLLEGES:
            logo_inline = get_college_logo_html(c["id"], size=18, border_radius="3px")
            st.markdown(
                f"<div style='font-size:0.75rem;color:#8ba3c7;padding:0.25rem 0;display:flex;align-items:center;gap:0.5rem'>"
                f"{logo_inline}"
                f"<span style='font-weight:600;color:var(--text-primary)'>{c['short']}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    if msg_count > 0:
        st.caption(f"\U0001f4ac {msg_count} message{'s' if msg_count != 1 else ''} this session")

    if st.button("\U0001f5d1\ufe0f Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.feedback_given = set()
        if st.session_state.get("chatbot") is not None:
            st.session_state.chatbot.clear_history(st.session_state.session_id)
            st.session_state.chatbot = None
        st.rerun()


# ── Page Router ───────────────────────────────────────────────────────────────
page = st.session_state.get("page", "\U0001f3e0 Overview")

if page == "\U0001f3e0 Overview":
    from pages.overview import render
    render()
elif page == "\U0001f4ac Chat":
    from pages.chat import render
    render()
elif page == "\u2696\ufe0f Compare":
    from pages.compare import render
    render()
elif page == "\U0001f4ca Dashboard":
    from pages.dashboard import render
    render()
elif page == "\U0001f4c5 Events":
    from pages.events import render
    render()
elif page == "\U0001f4de Contacts":
    from pages.contacts import render
    render()
elif page == "\U0001f4c8 Insights":
    from pages.insights import render
    render()
