"""
app.py — Main Streamlit Application for CampusAI Universal Campus Info Chatbot.
Premium 5-page interface with chat, dashboard, events, contacts, and analytics.
"""

import os
import sys
import json
import csv
import logging
import time
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Optional

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# ── Cloud-aware API key loader ────────────────────────────────────────────────
# Streamlit Cloud injects secrets via st.secrets (not .env).
# Push them into os.environ so all downstream libraries (LangChain, google-genai)
# can find them with os.getenv() as normal.
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass  # st.secrets not available locally — .env is used instead

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = ROOT / "data"

# ── Page Config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="CampusAI — Universal Campus Assistant",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/campus-ai",
        "About": "CampusAI — Universal Campus Information Assistant for Indian Colleges"
    }
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
def load_css():
    css_path = ROOT / "ui" / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    selected_col = st.session_state.get("selected_college")
    if selected_col:
        st.markdown("""
        <style>
        [data-testid="block-container"] {
          max-width: 850px !important;
          margin: 0 auto !important;
        }
        </style>
        """, unsafe_allow_html=True)

    dark = st.session_state.get("dark_mode", True)

    if dark:
        theme_css = """
        <style>
        :root {
          --bg-base:        #0F172A; /* Slate 900 */
          --bg-surface:     #1E293B; /* Slate 800 */
          --bg-card:        #1E293B;
          --text-primary:   #F8FAFC; /* Slate 50 */
          --text-secondary: #94A3B8; /* Slate 400 */
          --text-muted:     #475569; /* Slate 600 */
          --border:         #334155; /* Slate 700 */
          --accent:         #0052FF; /* Electric Blue */
          --accent-gradient: linear-gradient(135deg, #0052FF, #4D7CFF);
          --accent-fore:    #ffffff;
          --accent-sec:     #3B82F6; /* Slate Blue */
          --bg-sidebar:     #0F172A;
        }
        h1, h2, h3, h4, .calistoga-header {
          font-family: 'Calistoga', Georgia, serif !important;
          font-weight: 400 !important;
          letter-spacing: -0.01em !important;
        }
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
          color: var(--text-secondary) !important;
        }
        </style>
        """
    else:
        theme_css = """
        <style>
        :root {
          --bg-base:        #FAFAFA; /* Warm off-white */
          --bg-surface:     #ffffff; /* Pure white */
          --bg-card:        #ffffff;
          --text-primary:   #0F172A; /* Slate 900 */
          --text-secondary: #64748B; /* Slate 500 */
          --text-muted:     #94A3B8; /* Slate 400 */
          --border:         #E2E8F0; /* Slate 200 */
          --accent:         #0052FF; /* Electric Blue */
          --accent-gradient: linear-gradient(135deg, #0052FF, #4D7CFF);
          --accent-fore:    #ffffff;
          --accent-sec:     #3B82F6; /* Slate Blue */
          --bg-sidebar:     #F8FAFC; /* Slate 50 */
        }
        h1, h2, h3, h4, .calistoga-header {
          font-family: 'Calistoga', Georgia, serif !important;
          font-weight: 400 !important;
          letter-spacing: -0.01em !important;
        }
        /* Sidebar text: force readable dark color in light mode */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
          color: var(--text-primary) !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stRadioOption"]:has(input:checked) [data-testid="stMarkdownContainer"] p {
          color: var(--accent) !important;
        }
        /* Protect white text inside dark campus-header boxes */
        .campus-header h1, .campus-header h2,
        .campus-header [style*="color:#FFFFFF"],
        .campus-header [style*="color: #FFFFFF"] {
          color: #FFFFFF !important;
        }
        /* Keep inline-styled white text from being overridden */
        [style*="color:#FFFFFF"] { color: #FFFFFF !important; }
        [style*="color:#94A3B8"] { color: #94A3B8 !important; }
        [style*="color:#F8FAFC"] { color: #F8FAFC !important; }
        .message.bot .message-bubble {
          background: #ffffff !important;
          color: #09090b !important;
        }
        .message.user .message-bubble * {
          color: var(--accent-fore) !important;
        }
        </style>
        """

    static_overrides = """
    <style>
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"] > div,
    .main, .block-container {
      background-color: var(--bg-base) !important;
      color: var(--text-primary) !important;
    }

    .college-card-name, .info-card-title, .contact-name { color: var(--text-primary) !important; }
    .college-card-desc, .info-card-desc, .contact-dept, .contact-info { color: var(--text-secondary) !important; }
    
    .college-tag {
      background: rgba(0, 82, 255, 0.05) !important; 
      color: var(--accent) !important; 
      border: 1px solid rgba(0, 82, 255, 0.15) !important; 
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.70rem !important;
      padding: 0.2rem 0.6rem !important;
      border-radius: 6px !important;
    }

    .message.bot .message-bubble {
      background: var(--bg-surface) !important;
      border-color: var(--border) !important;
      color: var(--text-primary) !important;
    }
    .typing-indicator {
      background: var(--bg-surface) !important;
      border-color: var(--border) !important;
    }

    [data-testid="stTextInput"] input::placeholder { color: var(--text-secondary) !important; }

    [data-testid="stTabs"] [data-baseweb="tab-list"] {
      background: transparent !important;
      border-color: var(--border) !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] { color: var(--text-secondary) !important; }
    [data-testid="stTabs"] [aria-selected="true"] { color: var(--accent) !important; }

    [data-testid="stExpander"] {
      background-color: var(--bg-surface) !important;
      border-color: var(--border) !important;
      border-radius: 12px !important;
    }
    [data-testid="stExpander"] summary { color: var(--text-primary) !important; }

    [data-testid="stSelectbox"] > div,
    [data-testid="stSelectbox"] select {
      background-color: var(--bg-surface) !important;
      border-color: var(--border) !important;
      color: var(--text-primary) !important;
      border-radius: 8px !important;
    }

    /* Only color markdown text that does NOT have an explicit inline style */
    [data-testid="stMarkdownContainer"] > p,
    [data-testid="stMarkdownContainer"] li {
      color: var(--text-secondary);
    }
    /* Never override inline-styled text colors (dark boxes with white text etc.) */
    [data-testid="stMarkdownContainer"] [style*="color:"] {
      color: inherit;
    }

    hr { background-color: var(--border) !important; }

    /* ── Minimalist Modern Design Helpers ── */
    .section-label-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.65rem;
      border-radius: 9999px !important;
      border: 1px solid rgba(0, 82, 255, 0.25) !important;
      background: rgba(0, 82, 255, 0.05) !important;
      padding: 0.35rem 1.0rem !important;
      margin-bottom: 1.0rem !important;
    }
    .section-label-dot {
      display: inline-block;
      width: 7px;
      height: 7px;
      border-radius: 50% !important;
      background-color: var(--accent) !important;
      box-shadow: 0 0 6px var(--accent) !important;
    }
    .section-label-text {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.68rem !important;
      font-weight: 600 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.15em !important;
      color: var(--accent) !important;
    }

    .gradient-text {
      background: linear-gradient(135deg, #0052FF, #4D7CFF) !important;
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
      color: transparent !important;
      display: inline-block;
    }
    .gradient-underline-container {
      position: relative;
      display: inline-block;
    }
    .gradient-underline {
      position: absolute;
      bottom: -0.15rem;
      left: 0;
      height: 0.5rem;
      width: 100%;
      border-radius: 2px !important;
      background: linear-gradient(90deg, rgba(0, 82, 255, 0.25), rgba(77, 124, 255, 0.15)) !important;
      z-index: -1;
    }
    </style>
    """

    st.markdown(theme_css, unsafe_allow_html=True)
    st.markdown(static_overrides, unsafe_allow_html=True)



# ── Session State Initialization ──────────────────────────────────────────────
# ── College Registry ─────────────────────────────────────────────────────────
COLLEGES = [
    {
        "id": "general",
        "name": "General (All Indian Colleges)",
        "short": "General",
        "icon": "🇮🇳",
        "type": "Universal Guidelines",
        "location": "Pan-India",
        "color": "#4f8ef7",
        "desc": "Generic queries about any Indian college — attendance, CGPA, hostels, admissions, clubs, procedures.",
        "tags": ["Attendance", "CGPA", "Hostel", "Clubs", "Procedures"],
        "ranking": "Top 100 Overall",
        "students": "100k+ Active",
        "placement": "Multi-sector",
        "verified": True,
    },
    {
        "id": "iith",
        "name": "IIT Hyderabad (IITH)",
        "short": "IITH",
        "icon": "🔬",
        "type": "Central Government Institute",
        "location": "Kandi, Hyderabad",
        "color": "#f0883e",
        "desc": "Fractal Academics model, JEE admissions, fees, MCM scholarship, placements (₹90L highest), bus routes.",
        "tags": ["Fractal Academics", "JEE", "Scholarships", "Placements", "Bus Routes"],
        "ranking": "NIRF Eng #8",
        "students": "4,200+ Students",
        "placement": "₹90L Highest Package",
        "verified": True,
    },
    {
        "id": "iiith",
        "name": "IIIT Hyderabad (IIITH)",
        "short": "IIITH",
        "icon": "💻",
        "type": "Autonomous Deemed University (PPP)",
        "location": "Gachibowli, Hyderabad",
        "color": "#39c5b9",
        "desc": "Ada supercomputer (70 TFLOPS), UGEE/JEE admissions, 3 dining halls, placements (₹128L highest, ₹33.96L avg).",
        "tags": ["Supercomputer", "UGEE", "Dining", "Placements", "Hostels"],
        "ranking": "NIRF Eng #55",
        "students": "2,100+ Students",
        "placement": "₹1.28Cr Highest / ₹33.96L Avg",
        "verified": True,
    },
    {
        "id": "nalsar",
        "name": "NALSAR University of Law",
        "short": "NALSAR",
        "icon": "⚖️",
        "type": "National Law University",
        "location": "Hyderabad",
        "color": "#7c5cbf",
        "desc": "CLAT cutoff (Rank 1–130), fee structure (₹3.17L/yr), Ishan Uday & Indira Gandhi scholarships.",
        "tags": ["CLAT", "Law", "Scholarships", "Fees", "Admissions"],
        "ranking": "NIRF Law #3",
        "students": "1,200+ Students",
        "placement": "₹22L Avg Package",
        "verified": True,
    },
    {
        "id": "nims",
        "name": "NIMS — Nizam's Institute of Medical Sciences",
        "short": "NIMS",
        "icon": "🏥",
        "type": "Autonomous Medical University",
        "location": "Hyderabad",
        "color": "#3fb950",
        "desc": "MD/MS/DM/DNB/BPT programs, NEET PG cutoffs by category, NIMSET exam, fee ranges.",
        "tags": ["NEET PG", "MD", "MS", "DNB", "Cutoffs"],
        "ranking": "NIRF Medical #13",
        "students": "1,800+ Students",
        "placement": "Clinical Residencies",
        "verified": True,
    },
    {
        "id": "hcu",
        "name": "University of Hyderabad (HCU)",
        "short": "HCU",
        "icon": "🎓",
        "type": "Central University",
        "location": "Gachibowli, Hyderabad",
        "color": "#d29922",
        "desc": "2,300-acre campus, 23 hostels, Samarth portal, 50 km radius hostel rule, GRE/IELTS requirements.",
        "tags": ["Hostel", "Samarth Portal", "50km Rule", "GRE", "IELTS"],
        "ranking": "NIRF University #10",
        "students": "6,500+ Students",
        "placement": "Public R&D Placements",
        "verified": True,
    },
    {
        "id": "osmania",
        "name": "Osmania University",
        "short": "OU",
        "icon": "📜",
        "type": "State University",
        "location": "Hyderabad",
        "color": "#e3b341",
        "desc": "CBCS rules, SGPA/CGPA formulas, 75% attendance, 20% internal assessment, dual examiner system.",
        "tags": ["CBCS", "SGPA", "CGPA", "Attendance", "Internal Marks"],
        "ranking": "NIRF University #36",
        "students": "15,000+ Students",
        "placement": "IT & Core Recruiters",
        "verified": True,
    },
    {
        "id": "bits_hyd",
        "name": "BITS Pilani — Hyderabad Campus",
        "short": "BITS Hyd",
        "icon": "🏛️",
        "type": "Private Deemed University",
        "location": "Shameerpet, Hyderabad",
        "color": "#58a6ff",
        "desc": "200-acre residential campus, 15,000 sq ft commercial complex, 24/7 medical center (Medicity tie-up).",
        "tags": ["Residential", "Campus Shops", "Medical", "SBI ATM", "Post Office"],
        "ranking": "NIRF Eng #25",
        "students": "3,500+ Students",
        "placement": "₹60.75L Highest / ₹30L Avg CSE",
        "verified": True,
    },
    {
        "id": "isb_hyd",
        "name": "Indian School of Business (ISB) Hyderabad",
        "short": "ISB Hyd",
        "icon": "💼",
        "type": "Private Business School",
        "location": "Gachibowli, Hyderabad",
        "color": "#7c5cbf",
        "desc": "AACSB & SAQS accredited flagship 1-year PGP equivalent to a global MBA, domestic average package of ₹33.25 LPA, highest ₹1.56 Crore.",
        "tags": ["MBA", "PGP", "AACSB", "Placements", "Consulting"],
        "ranking": "FT Global MBA #31",
        "students": "900+ Students",
        "placement": "₹1.56 Crore Highest Package",
        "verified": True,
    },
    {
        "id": "imt_hyd",
        "name": "IMT Hyderabad",
        "short": "IMT Hyd",
        "icon": "📈",
        "type": "Private Business School",
        "location": "Shamshabad, Hyderabad",
        "color": "#f0883e",
        "desc": "30-acre green campus, 2-year PGDM programs, 14-week corporate internships, scholarships including 95% waiver for EWS and female diversity refunds.",
        "tags": ["PGDM", "Internships", "Scholarships", "Residential", "AICTE"],
        "ranking": "NIRF Mgmt #84",
        "students": "480+ Students",
        "placement": "₹25.0L Highest Package",
        "verified": True,
    },
    {
        "id": "ibs_hyd",
        "name": "ICFAI Business School (IBS) Hyderabad",
        "short": "IBS Hyd",
        "icon": "📊",
        "type": "Private Business School",
        "location": "Donthanapally, Hyderabad",
        "color": "#39c5b9",
        "desc": "91-acre campus, AACSB & NAAC A++ accredited MBA, case-study pedagogy with 6,000+ case studies, placement average of ₹9.82 LPA.",
        "tags": ["MBA", "Case Study", "AACSB", "Placements", "NAAC A++"],
        "ranking": "NIRF Mgmt #40",
        "students": "2,400+ Students",
        "placement": "₹21.0L Highest / ₹9.82L Avg",
        "verified": True,
    },
    {
        "id": "omc",
        "name": "Osmania Medical College (OMC)",
        "short": "OMC",
        "icon": "🩺",
        "type": "Government Medical College",
        "location": "Koti, Hyderabad",
        "color": "#3fb950",
        "desc": "Established in 1846, central node for 10 specialized teaching hospitals (6,000+ beds), ₹10,000/yr tuition, 1-year service bond with ₹20L penalty.",
        "tags": ["NEET", "MBBS", "MD/MS", "Service Bond", "Clinical Exposure"],
        "ranking": "NIRF Medical #25",
        "students": "1,250+ Students",
        "placement": "Clinicals in 10 teaching hospitals",
        "verified": True,
    },
    {
        "id": "nizam",
        "name": "Nizam College Hyderabad",
        "short": "Nizam",
        "icon": "🏛️",
        "type": "Constituent College of Osmania University",
        "location": "Basheerbagh, Hyderabad",
        "color": "#d29922",
        "desc": "Established in 1887, 20-acre historical campus, regular and self-financed UG/PG programs (e.g. B.Sc Data Science), TASK-registered placements.",
        "tags": ["DOST", "B.Sc Data Science", "Autonomous", "TASK Placements", "Hostel"],
        "ranking": "Arts Band 51-100",
        "students": "2,200+ Students",
        "placement": "TASK Placements cell",
        "verified": True,
    },
    {
        "id": "st_francis",
        "name": "St. Francis College for Women",
        "short": "St. Francis",
        "icon": "👩‍🎓",
        "type": "Autonomous Minority College",
        "location": "Begumpet, Hyderabad",
        "color": "#4f8ef7",
        "desc": "Established in 1959, NAAC A++ grade, online admissions with minority policies, median UG package of ₹4.0 LPA and PG package of ₹7.60 LPA.",
        "tags": ["NAAC A++", "Women", "Admissions", "Placements", "Minority Quota"],
        "ranking": "NAAC A++ Grade",
        "students": "3,000+ Students",
        "placement": "₹7.60L PG Avg Package",
        "verified": True,
    },
    {
        "id": "jntuh",
        "name": "JNTU Hyderabad (JNTUH)",
        "short": "JNTUH",
        "icon": "⚙️",
        "type": "State University",
        "location": "Kukatpally, Hyderabad",
        "color": "#e3b341",
        "desc": "State-level engineering pathway via TS EAMCET, offers B.Tech/M.Tech programs, average placement package of ₹6.00 LPA.",
        "tags": ["TS EAMCET", "State University", "B.Tech", "Placements"],
        "ranking": "NIRF Eng #83",
        "students": "8,000+ Students",
        "placement": "₹6.00L Avg Package",
        "verified": True,
    },
    {
        "id": "cbit",
        "name": "Chaitanya Bharathi Institute of Technology (CBIT)",
        "short": "CBIT",
        "icon": "🏫",
        "type": "Autonomous Private Institute",
        "location": "Gandipet, Hyderabad",
        "color": "#4f8ef7",
        "desc": "Top autonomous engineering college, TS EAMCET/JEE admissions, B.Tech intake of 1,700+ students, highest CTC of ₹54.00 LPA, average CSE ₹6.50 LPA.",
        "tags": ["TS EAMCET", "Gandipet", "Autonomous", "Placements", "Engineering"],
        "ranking": "NIRF Eng #151",
        "students": "5,400+ Students",
        "placement": "₹54.0L Highest / ₹6.50L Avg",
        "verified": True,
    },
    {
        "id": "griet",
        "name": "Gokaraju Rangaraju Institute (GRIET)",
        "short": "GRIET",
        "icon": "📐",
        "type": "Autonomous Private Institute",
        "location": "Bachupally, Hyderabad",
        "color": "#f0883e",
        "desc": "Autonomous engineering college, TS EAMCET admissions, B.Tech average package of ₹9.27 LPA, highest package of ₹51.60 LPA.",
        "tags": ["TS EAMCET", "Bachupally", "Placements", "Autonomous"],
        "ranking": "NIRF Eng #165",
        "students": "4,500+ Students",
        "placement": "₹51.60L Highest / ₹9.27L Avg",
        "verified": True,
    },
    {
        "id": "vnr_vjiet",
        "name": "VNR VJIET",
        "short": "VNR VJIET",
        "icon": "🧪",
        "type": "Autonomous Private Institute",
        "location": "Bachupally, Hyderabad",
        "color": "#39c5b9",
        "desc": "Autonomous engineering college, admissions via TS EAMCET, high-capacity B.Tech intake of 1,900+ students, average package of ₹6.00 LPA.",
        "tags": ["TS EAMCET", "Bachupally", "High Intake", "Placements"],
        "ranking": "NIRF Eng #101",
        "students": "6,000+ Students",
        "placement": "₹48.00L Highest / ₹6.00L Avg",
        "verified": True,
    },
    {
        "id": "vardhaman",
        "name": "Vardhaman College of Engineering",
        "short": "Vardhaman",
        "icon": "🔬",
        "type": "Autonomous Private Institute",
        "location": "Shamshabad, Hyderabad",
        "color": "#3fb950",
        "desc": "Autonomous engineering college, TS EAMCET admissions, median placement package of ₹6.25 LPA, average package of ₹5.74 LPA for CSE.",
        "tags": ["TS EAMCET", "Shamshabad", "Autonomous", "Placements"],
        "ranking": "NIRF Eng #143",
        "students": "3,800+ Students",
        "placement": "₹6.25L Median Package",
        "verified": True,
    },
    {
        "id": "anurag",
        "name": "Anurag University",
        "short": "Anurag",
        "icon": "🛰️",
        "type": "Private University",
        "location": "Venkatapur, Hyderabad",
        "color": "#7c5cbf",
        "desc": "Private university, admissions via TS EAMCET and JEE Main, offers B.Tech programs, average placement package of ₹5.20 LPA.",
        "tags": ["TS EAMCET", "JEE Main", "Private University", "Placements"],
        "ranking": "NIRF Eng #150",
        "students": "5,000+ Students",
        "placement": "₹5.20L Avg Package",
        "verified": True,
    },
    {
        "id": "iare",
        "name": "Institute of Aeronautical Engineering (IARE)",
        "short": "IARE",
        "icon": "✈️",
        "type": "Autonomous Private Institute",
        "location": "Dundigal, Hyderabad",
        "color": "#58a6ff",
        "desc": "Autonomous engineering college, admissions via TS EAMCET, average package of ₹7.00 LPA for CSE, highest package of ₹60.00 LPA.",
        "tags": ["TS EAMCET", "Dundigal", "Aeronautical", "Placements"],
    },
]

COLLEGE_MAP = {c["id"]: c for c in COLLEGES}


def init_session_state():
    defaults = {
        "messages": [],           # List of {role, content, timestamp, tool_used, query_id}
        "session_id": str(uuid.uuid4()),
        "chatbot": None,
        "db_initialized": False,
        "vs_loaded": False,
        "page": "🏠 Overview",
        "feedback_given": set(),
        "contact_filter": "",
        "event_filter": "all",
        "selected_college": None,   # None = not yet chosen
        "dark_mode": False,
        "last_selected_college": None,
        "last_page": "🏠 Overview",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()
# Force light mode as the default — overwrite any stale dark_mode=True from old sessions
if st.session_state.get("dark_mode", False) is True and "dark_mode_v2" not in st.session_state:
    st.session_state.dark_mode = False
    st.session_state.dark_mode_v2 = True  # sentinel so we only reset once
load_css()



# ── Database & Chatbot Initialization ─────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_database():
    from core.database import initialize_database
    initialize_database()
    return True

@st.cache_resource(show_spinner=False)
def get_chatbot():
    from core.agent import CampusChatbot
    bot = CampusChatbot()
    return bot

@st.cache_resource(show_spinner=False)
def check_vector_store():
    from core.embeddings import get_vector_store
    vs = get_vector_store()
    return vs.is_ready

@st.cache_resource(show_spinner=False)
def get_vector_store_docs_count():
    try:
        from core.embeddings import get_vector_store
        vs = get_vector_store()
        return len(vs.documents)
    except Exception:
        return 0

# Initialize resources
try:
    get_database()
    st.session_state.db_initialized = True
except Exception as e:
    logger.error(f"DB init failed: {e}")

# ── Helper Functions ──────────────────────────────────────────────────────────

def get_college_icon_html(icon_emoji: str, size: int = 22, color: str = "var(--accent)") -> str:
    """Helper to convert emoji to a high-fidelity outline SVG icon for premium rendering."""
    svg_map = {
        "🔬": '<path d="M6 18h8M3 22h14M12 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM12 9v13M9 3h3"/>', 
        "💻": '<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>', 
        "⚖️": '<path d="M16 16c0 2-3 3-3 3s-3-1-3-3m0-12h6M12 3v16m-8-3c0 2 3 3 3 3s3-1 3-3m-3-1c-1.5 0-3 1-3 3m9-3c1.5 0 3 1 3 3"/>', 
        "🏥": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 8v8M8 12h8"/>', 
        "🎓": '<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/><path d="M22 10v6"/>', 
        "📜": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>', 
        "🏛️": '<path d="M4 22h16M10 14h4M4 18h16M12 2L2 7h20L12 2zM5 14v4M9 14v4M13 14v4M17 14v4"/>', 
        "💼": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>', 
        "📈": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>', 
        "📊": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>', 
        "🩺": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>', 
        "👩‍🎓": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 10L17 7.5L12 10l5 2.5L22 10z"/>', 
        "⚙️": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>', 
        "📐": '<path d="M21.3 8.3L15.7 2.7a2 2 0 0 0-2.8 0L2.7 12.9a2 2 0 0 0 0 2.8l5.6 5.6a2 2 0 0 0 2.8 0L21.3 11.1a2 2 0 0 0 0-2.8zM8.3 18.5l-2.8-2.8"/>', 
        "🛰️": '<path d="M12 2L2 22l10-6 10 6L12 2z"/>', 
        "✈️": '<path d="M21 16V8a2 2 0 0 0-2-2h-3L9 12H3a2 2 0 0 0 0 4h6l7 6h3a2 2 0 0 0 2-2v-2"/>', 
        "🇮🇳": '<path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/>', 
        "🗺️": '<path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/>', 
        "🏠": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>', 
        "📞": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>', 
        "📅": '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>', 
        "🎭": '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>'
    }
    path = svg_map.get(icon_emoji, '<circle cx="12" cy="12" r="10"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;filter:drop-shadow(0 0 4px {color}40);">{path}</svg>'.strip()


def get_college_logo_html(college_id: str, size: int = 32, border_radius: str = "6px") -> str:
    """Renders a stylized monogram or emblem representing the institution."""
    logo_map = {
        "general": ("GEN", "rgba(0, 82, 255, 0.05)", "var(--accent)"),
        "iith": ("IITH", "rgba(240, 136, 62, 0.05)", "#f0883e"),
        "iiith": ("IIITH", "rgba(57, 197, 185, 0.05)", "#39c5b9"),
        "nalsar": ("LAW", "rgba(124, 92, 191, 0.05)", "#7c5cbf"),
        "nims": ("NIMS", "rgba(63, 185, 80, 0.05)", "#3fb950"),
        "hcu": ("HCU", "rgba(210, 153, 34, 0.05)", "#d29922"),
        "osmania": ("OU", "rgba(227, 179, 65, 0.05)", "#e3b341"),
        "bits_hyd": ("BITS", "rgba(88, 166, 255, 0.05)", "#58a6ff"),
        "isb_hyd": ("ISB", "rgba(124, 92, 191, 0.05)", "#7c5cbf"),
        "imt_hyd": ("IMT", "rgba(240, 136, 62, 0.05)", "#f0883e"),
        "ibs_hyd": ("IBS", "rgba(57, 197, 185, 0.05)", "#39c5b9"),
        "omc": ("OMC", "rgba(63, 185, 80, 0.05)", "#3fb950"),
        "nizam": ("NIZAM", "rgba(210, 153, 34, 0.05)", "#d29922"),
        "st_francis": ("SFC", "rgba(79, 142, 247, 0.05)", "#4f8ef7"),
        "jntuh": ("JNTUH", "rgba(227, 179, 65, 0.05)", "#e3b341"),
        "cbit": ("CBIT", "rgba(79, 142, 247, 0.05)", "#4f8ef7"),
        "griet": ("GRIET", "rgba(240, 136, 62, 0.05)", "#f0883e"),
        "vnr_vjiet": ("VNR", "rgba(57, 197, 185, 0.05)", "#39c5b9"),
        "vardhaman": ("VCE", "rgba(63, 185, 80, 0.05)", "#3fb950"),
        "anurag": ("AU", "rgba(124, 92, 191, 0.05)", "#7c5cbf"),
        "iare": ("IARE", "rgba(88, 166, 255, 0.05)", "#58a6ff"),
    }
    label, bg, color = logo_map.get(college_id, ("CAMPUS", "rgba(0, 82, 255, 0.05)", "var(--accent)"))
    
    # Custom vector crests for top universities to look highly authentic
    if college_id == "iiith":
        return f"""
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#39c5b9;filter:drop-shadow(0 0 4px rgba(57,197,185,0.3))">
                <path d="M12 2L2 12l10 10 10-10L12 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 6l6 6-6 6-6-6 6-6z" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">IIIT</span>
        </div>
        """.strip()
    elif college_id == "iith":
        return f"""
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#f0883e;filter:drop-shadow(0 0 4px rgba(240,136,62,0.3))">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 2"/>
                <circle cx="12" cy="12" r="2" fill="currentColor"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">IIT-H</span>
        </div>
        """.strip()
    elif college_id == "nalsar":
        return f"""
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#7c5cbf;filter:drop-shadow(0 0 4px rgba(124,92,191,0.3))">
                <path d="M3 21h18M5 21V10M19 21V10M9 21V10M15 21V10M4 6h16M12 3L3 6h18l-9-3z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">NALSAR</span>
        </div>
        """.strip()
    elif college_id == "hcu":
        return f"""
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#d29922;filter:drop-shadow(0 0 4px rgba(210,153,34,0.3))">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 0 6.5 22H20M4 19.5V4.5A2.5 2.5 0 0 1 6.5 2V17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 6v6M9 9h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">HCU</span>
        </div>
        """.strip()
    elif college_id == "bits_hyd":
        return f"""
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#58a6ff;filter:drop-shadow(0 0 4px rgba(88,166,255,0.3))">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">BITS</span>
        </div>
        """.strip()

    # Monogram Fallbacks
    return f"""
    <div class="college-logo-badge" style="width:{size}px;height:{size}px;background:{bg};border:1px solid {color}33;color:{color};border-radius:{border_radius};">
        {label}
    </div>
    """.strip()


def get_button_emoji(icon_emoji: str) -> str:
    """Helper to return an alternative broadly-supported emoji for native buttons where HTML is escaped."""
    return "🏫" if icon_emoji == "🎓" else icon_emoji


def render_message(msg: dict, idx: int):
    """Render a single chat message bubble with HTML."""
    role = msg["role"]
    content = msg["content"]
    timestamp = msg.get("timestamp", "")
    tool = msg.get("tool_used", "")

    if role == "user":
        st.markdown(f"""
        <div class="message user">
            <div class="message-avatar">👤</div>
            <div>
                <div class="message-bubble">{content}</div>
                <div class="message-meta" style="text-align:right">{timestamp}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        tool_badge = f'<span class="event-badge badge-academic" style="margin-left:0.5rem">{tool}</span>' if tool else ""
        st.markdown(f"""
        <div class="message bot">
            <div class="message-avatar">{get_college_icon_html("🎓")}</div>
            <div style="width:100%">
                <div class="message-bubble">{content}</div>
                <div class="message-meta">{timestamp} {tool_badge}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Feedback buttons
        if idx not in st.session_state.feedback_given:
            col1, col2, col3 = st.columns([1, 0.15, 0.15])
            with col2:
                if st.button("👍", key=f"up_{idx}", help="Helpful"):
                    _give_feedback(msg.get("query_id"), 1, idx)
            with col3:
                if st.button("👎", key=f"dn_{idx}", help="Not helpful"):
                    _give_feedback(msg.get("query_id"), -1, idx)


def _give_feedback(query_id: Optional[int], rating: int, msg_idx: int):
    """Record user feedback in the database."""
    try:
        from core.database import log_feedback
        if query_id:
            log_feedback(query_id, rating)
        st.session_state.feedback_given.add(msg_idx)
        st.success("✅ Thanks for your feedback!" if rating == 1 else "📝 Feedback recorded. We'll improve!")
    except Exception as e:
        logger.error(f"Feedback error: {e}")


def send_message(user_input: str):
    """Process a user message through the chatbot and update session state."""
    if not user_input.strip():
        return

    # Check API key
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_new_groq_key_here":
        st.error("⚠️ **Groq API Key not configured!** Please add your `GROQ_API_KEY` to the `.env` file and restart.")
        return

    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp,
    })

    # Build college-aware query
    college = st.session_state.get("selected_college")
    if college and college != "general":
        college_info = COLLEGE_MAP.get(college, {})
        college_name = college_info.get("name", college)
        contextual_input = (
            f"[Context: The student is asking about {college_name}. "
            f"Focus your answer specifically on {college_name} when relevant data is available. "
            f"If the specific detail is not in your knowledge base for this institution, "
            f"provide general Indian college guidance and note it may vary.]\n\n"
            f"Student question: {user_input}"
        )
    else:
        contextual_input = user_input

    # Get chatbot response — show typing indicator while waiting
    typing_placeholder = st.empty()
    typing_placeholder.markdown(f"""
        <div class="message bot">
            <div class="message-avatar">{get_college_icon_html("🎓")}</div>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    try:
        chatbot = get_chatbot()
        response, tool_used, resp_time_ms = chatbot.chat(
            contextual_input,
            session_id=st.session_state.session_id
        )

        # Log to database
        query_id = None
        try:
            from core.agent import categorize_query
            from core.database import log_query
            category = categorize_query(user_input)
            query_id = log_query(
                session_id=st.session_state.session_id,
                user_query=user_input,
                bot_response=response,
                tool_used=tool_used,
                category=category,
                response_time_ms=resp_time_ms
            )
        except Exception as e:
            logger.error(f"DB logging error: {e}")

    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        response = (
            "🔧 **System Error**: I'm having trouble connecting right now.\n\n"
            "Please check:\n"
            "1. Your `GROQ_API_KEY` is valid in `.env`\n"
            "2. The vector store is initialized (`python initialize.py`)\n"
            "3. All dependencies are installed (`pip install -r requirements.txt`)"
        )
        tool_used = ""
        query_id = None
        resp_time_ms = 0

    # Clear the typing indicator
    typing_placeholder.empty()


    # Add bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime("%H:%M"),
        "tool_used": tool_used,
        "query_id": query_id,
        "response_time_ms": resp_time_ms,
    })


def load_contacts() -> list:
    """Load contact directory from CSV."""
    try:
        contacts_file = DATA_DIR / "contacts" / "directory.csv"
        with open(contacts_file, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def load_events() -> list:
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
    except Exception:
        return []


# ── Sidebar ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Theme toggle at the top
    is_dark = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    if is_dark != st.session_state.dark_mode:
        st.session_state.dark_mode = is_dark
        st.rerun()
    st.markdown("<div style='margin-bottom:0.75rem'></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    # Brand — graduation cap SVG + name
    st.markdown("""
    <div style="
        display:flex;
        align-items:center;
        gap:0.85rem;
        padding:1.1rem 0 1.4rem 0;
        border-bottom:1px solid var(--border);
        margin-bottom:1.5rem;
    ">
        <!-- CAI Logo tile with graduation cap SVG -->
        <div style="
            width:44px; height:44px;
            background:linear-gradient(135deg,#0052FF,#4D7CFF);
            border-radius:10px;
            display:flex;
            align-items:center;
            justify-content:center;
            flex-shrink:0;
            box-shadow:0 4px 12px rgba(0,82,255,0.28);
        ">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- Graduation cap diamond -->
                <path d="M12 3L22 8.5L12 14L2 8.5L12 3Z" stroke="white" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>
                <!-- Gown curve -->
                <path d="M6 11V16.5C8.5 18.8 15.5 18.8 18 16.5V11" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                <!-- Tassel cord -->
                <line x1="22" y1="8.5" x2="22" y2="13" stroke="white" stroke-width="1.6" stroke-linecap="round"/>
                <circle cx="22" cy="14" r="1.1" fill="white"/>
            </svg>
        </div>
        <!-- Name + tagline -->
        <div>
            <div style="
                font-family:'Calistoga',Georgia,serif;
                font-size:1.22rem;
                font-weight:400;
                color:var(--text-primary);
                letter-spacing:-0.01em;
                line-height:1.2;
            ">CampusAI</div>
            <div style="
                font-size:0.62rem;
                color:var(--text-secondary);
                text-transform:uppercase;
                letter-spacing:0.08em;
                font-weight:600;
                margin-top:0.15rem;
                font-family:'Inter',sans-serif;
            ">Verified College Intelligence</div>
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
            <div style="font-size:1.0rem;font-weight:600;color:var(--text-primary);letter-spacing:-0.01em;margin-top:0.25rem">{c_info.get('short','—')}</div>
            <div style="font-size:0.65rem;color:var(--text-secondary);margin-top:0.1rem">{c_info.get('type','')}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Switch College", use_container_width=True):
            st.session_state.selected_college = None
            st.session_state.messages = []
            st.session_state.feedback_given = set()
            try:
                get_chatbot().clear_history()
            except Exception:
                pass
            st.rerun()
        st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    # Navigation — Linear-style clean text labels
    pages = ["🏠 Overview", "💬 Chat", "⚖️ Compare", "📊 Dashboard", "📅 Events", "📞 Contacts", "📈 Insights"]
    _page_labels = {
        "🏠 Overview":  "Overview",
        "💬 Chat":      "Chat",
        "⚖️ Compare":   "Compare",
        "📊 Dashboard": "Dashboard",
        "📅 Events":    "Events",
        "📞 Contacts":  "Contacts",
        "📈 Insights":  "Insights",
    }
    selected_page = st.radio(
        "Navigate",
        pages,
        index=pages.index(st.session_state.page) if st.session_state.page in pages else 0,
        label_visibility="collapsed",
        format_func=lambda x: _page_labels.get(x, x)
    )
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)

    # System status
    api_key = os.getenv("GROQ_API_KEY", "")
    api_ok = bool(api_key and api_key != "your_new_groq_key_here")
    try:
        vs_ready = check_vector_store()
    except Exception:
        vs_ready = False

    status_color = "#10b981" if api_ok else "#ef4444"
    status_text = "Groq Online" if api_ok else "Groq Offline"
    status_emoji = "🟢" if api_ok else "🔴"
    
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
                <span>📚</span>
                <span>{get_vector_store_docs_count() if vs_ready else 0} Chunks</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span>🏫</span>
                <span>{len(COLLEGES)} Colleges</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)

    with st.expander("🏫 Indexed Colleges", expanded=False):
        for c in COLLEGES:
            logo_inline = get_college_logo_html(c['id'], size=18, border_radius="3px")
            st.markdown(
                f"<div style='font-size:0.75rem;color:#8ba3c7;padding:0.25rem 0;display:flex;align-items:center;gap:0.5rem'>"
                f"{logo_inline}"
                f"<span style='font-weight:600;color:var(--text-primary)'>{c['short']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

    msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    if msg_count > 0:
        st.caption(f"💬 {msg_count} message{'s' if msg_count != 1 else ''} this session")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.feedback_given = set()
        try:
            get_chatbot().clear_history()
        except Exception:
            pass
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# COLLEGE SELECTION SCREEN
# ══════════════════════════════════════════════════════════════════════════════
# ==============================================================================
# PAGE: OVERVIEW
# ==============================================================================
if st.session_state.page == "🏠 Overview":

    st.markdown(f"""
<div style="
    background-color:#0F172A;
    background-image:radial-gradient(rgba(255,255,255,0.04) 1px,transparent 1px);
    background-size:24px 24px;
    border:1px solid #1E293B;
    border-radius:16px;
    padding:2.5rem 3rem;
    margin-bottom:2rem;
    box-shadow:0 20px 40px rgba(0,0,0,0.3);
">
    <div style="
        display:inline-flex;
        align-items:center;
        gap:0.6rem;
        border:1px solid rgba(0,82,255,0.35);
        background:rgba(0,82,255,0.08);
        border-radius:9999px;
        padding:0.3rem 1rem;
        margin-bottom:1.25rem;
    ">
        <span style="
            display:inline-block;
            width:7px;height:7px;
            border-radius:50%;
            background:#0052FF;
            box-shadow:0 0 6px #0052FF;
        "></span>
        <span style="
            font-family:'JetBrains Mono',monospace;
            font-size:0.68rem;font-weight:600;
            text-transform:uppercase;letter-spacing:0.15em;
            color:#60a5fa;
        ">CampusAI — Verified Intelligence</span>
    </div>
    <div style="
        font-size:2.5rem;font-weight:400;
        font-family:'Calistoga',Georgia,serif;
        letter-spacing:-0.02em;
        line-height:1.2;
        color:#FFFFFF;
        margin:0 0 1.1rem 0;
    ">
        Get instant answers about admissions, placements, fees, hostels, and campus life from
        <span style="
            background:linear-gradient(135deg,#60a5fa,#818cf8);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            color:transparent;
        ">verified college data</span>.
    </div>
    <div style="color:#94A3B8;font-size:1.0rem;line-height:1.65;max-width:800px;font-family:'Inter',sans-serif;">
        Unlike general-purpose models (like ChatGPT) which hallucinate and use outdated data, CampusAI
        retrieves answers directly from official college reports, NIRF submittals, and handbooks with strict
        source citations.
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Hero CTA buttons ──────────────────────────────────────────
    cta1, cta2, _pad = st.columns([1.3, 1.6, 3])
    with cta1:
        if st.button("Start Chat →", use_container_width=True, key="hero_chat"):
            st.session_state.page = "💬 Chat"
            st.rerun()
    with cta2:
        if st.button("Compare Colleges", use_container_width=True, key="hero_compare"):
            st.session_state.page = "⚖️ Compare"
            st.rerun()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        st.markdown("""
        <div style="background:var(--bg-surface);border:1px solid var(--border);padding:1.5rem;border-radius:12px;height:100%;">
            <div style="font-weight:600;font-size:1rem;color:var(--accent);margin-bottom:0.5rem;">🎯 AI Capability Showcase & Suggested Queries</div>
            <div style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;">
                • Compare placement packages (e.g. <i>"Compare highest CTC between IIT-H and IIIT-H"</i>)<br>
                • Get fee breakdown (e.g. <i>"What are the hostel and tuition fees at NALSAR?"</i>)<br>
                • Research scholarships (e.g. <i>"Which scholarships are available at HCU?"</i>)<br>
                • Find eligibility cutoffs (e.g. <i>"CLAT cutoff rank for NALSAR"</i>)
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_cap2:
        st.markdown("""
        <div style="background:var(--bg-surface);border:1px solid var(--border);padding:1.5rem;border-radius:12px;height:100%;">
            <div style="font-weight:600;font-size:1rem;color:var(--accent);margin-bottom:0.5rem;">🔒 Why Trust CampusAI?</div>
            <p style="margin:0;font-size:0.85rem;color:var(--text-secondary);line-height:1.5;">
                All answer retrieval parameters are restricted to <strong>official documents only</strong>: university handbooks, NIRF statistics, placement reports, fee structures, and verified brochures. Every response appends exact filename citations for accountability.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # Comparator promo banner
    st.markdown(f"""
    <div style="background:var(--bg-surface); border:1px solid var(--border); padding:1.5rem; border-radius:12px; margin-bottom: 2.5rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.02);">
        <div>
            <div style="font-weight:600; font-size:1.15rem; color:var(--text-primary); margin-bottom:0.25rem; font-family:'Calistoga',serif;">Compare Colleges Instantly</div>
            <div style="font-size:0.88rem; color:var(--text-secondary);">Analyze fees, placements, ratings, and student count side-by-side.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    comp_col1, comp_col2 = st.columns([4, 1])
    with comp_col2:
        if st.button("⚖️ Compare Page", use_container_width=True):
            st.session_state.page = "⚖️ Compare"
            st.rerun()

    st.markdown("""
    <div class="section-label-badge" style="margin-top: 1rem;">
        <span class="section-label-dot"></span>
        <span class="section-label-text">Directory</span>
    </div>
    <h2 style="font-family:'Calistoga',serif !important; font-weight:400; font-size:1.85rem; margin-top:0.25rem; margin-bottom:1.5rem; color:var(--text-primary);">Browse Verified College Intelligence</h2>
    """, unsafe_allow_html=True)

    # College cards — 3 columns
    for row_start in range(0, len(COLLEGES), 3):
        row_colleges = COLLEGES[row_start:row_start + 3]
        cols = st.columns(3)
        for i, c in enumerate(row_colleges):
            with cols[i]:
                verified_badge = '<span style="font-size:0.6rem;font-weight:600;color:#10b981;background:rgba(16,185,129,0.08);padding:0.15rem 0.45rem;border-radius:4px;border:1px solid rgba(16,185,129,0.15);">✓ VERIFIED SOURCE</span>'
                logo_html = get_college_logo_html(c['id'], size=36)
                icon_html = get_college_icon_html(c['icon'], size=20)
                
                st.markdown(f"""
                <div class="college-card-content">
                    <div class="college-card-header">
                        <div style="display:flex;justify-content:space-between;width:100%;align-items:center;">
                            <div class="college-logo">{logo_html}</div>
                            {verified_badge}
                        </div>
                        <div style="display:flex; justify-content:space-between; width:100%; align-items:center; margin-top: 0.25rem;">
                            <div class="college-card-type">{c['type']}</div>
                            <div class="college-card-icon">{icon_html}</div>
                        </div>
                        <div class="college-card-name">{c['name']}</div>
                    </div>
                    <div style="font-size: 0.9rem; line-height: 1.55; color: var(--text-secondary); display: flex; flex-direction: column; gap: 0.35rem; margin-top: 0.25rem;">
                        <div style="font-weight: 600; color: var(--text-primary);">🏆 {c.get('ranking', 'N/A')}</div>
                        <div>👥 {c.get('students', 'N/A')}</div>
                        <div style="font-weight: 500; color: var(--accent);">💼 {c.get('placement', 'N/A')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(
                    "View Details →",
                    key=f"select_{c['id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_college = c["id"]
                    st.session_state.messages = []
                    st.session_state.page = "💬 Chat"
                    st.rerun()



# ==============================================================================
# PAGE: COMPARE
# ==============================================================================
if st.session_state.page == "⚖️ Compare":
    st.markdown(f"""
    <div class="campus-header" style="background-color: #0F172A !important; background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important; background-size: 24px 24px !important; color: #F8FAFC !important; border-color: #1E293B !important; padding: 2.25rem !important; border-radius: 16px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;">
        <div class="section-label-badge">
            <span class="section-label-dot"></span>
            <span class="section-label-text">Compare</span>
        </div>
        <h1 style="font-size:2.0rem;font-weight:400;font-family:'Calistoga',serif !important;color:#FFFFFF !important;margin:0 0 0.75rem 0;letter-spacing:-0.01em;">Compare Colleges Instantly</h1>
        <p style="color:#94A3B8 !important;margin:0;">Select any two institutions to compare their placement records, tuition, student population, rankings, and cutoffs side-by-side.</p>
    </div>
    """, unsafe_allow_html=True)

    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        comp_id1 = st.selectbox("Select College 1", [c["name"] for c in COLLEGES], index=1, key="comp_1")
    with col_sel2:
        comp_id2 = st.selectbox("Select College 2", [c["name"] for c in COLLEGES], index=2, key="comp_2")

    c1 = next(c for c in COLLEGES if c["name"] == comp_id1)
    c2 = next(c for c in COLLEGES if c["name"] == comp_id2)

    if c1 and c2:
        comp_data = {
            "Comparison Category": ["Short Name", "Type", "Location", "NIRF Ranking", "Student Count", "Placement CTC / Highlights"],
            c1["name"]: [c1["short"], c1["type"], c1["location"], c1.get("ranking", "N/A"), c1.get("students", "N/A"), c1.get("placement", "N/A")],
            c2["name"]: [c2["short"], c2["type"], c2["location"], c2.get("ranking", "N/A"), c2.get("students", "N/A"), c2.get("placement", "N/A")]
        }
        df_comp = pd.DataFrame(comp_data)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)


# ==============================================================================
# PAGE: CHAT
# ==============================================================================
if st.session_state.page == "💬 Chat":
    # Always initialise active_c so it is available regardless of branch taken below
    active_c = COLLEGE_MAP.get(st.session_state.get("selected_college") or "", {})
    college_color = active_c.get('color', '#6366f1')

    if st.session_state.get("selected_college") is None:
        st.markdown(f"""
<div style="background-color:#0F172A;background-image:radial-gradient(rgba(255,255,255,0.04) 1px,transparent 1px);background-size:24px 24px;border:1px solid #1E293B;border-radius:16px;padding:2.25rem;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin-bottom:1.5rem;">
    <div style="display:inline-flex;align-items:center;gap:0.6rem;border:1px solid rgba(0,82,255,0.35);background:rgba(0,82,255,0.08);border-radius:9999px;padding:0.3rem 1rem;margin-bottom:1rem;">
        <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#0052FF;box-shadow:0 0 6px #0052FF;"></span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.15em;color:#60a5fa;">CampusAI Assistant</span>
    </div>
    <div style="font-size:2.0rem;font-weight:400;font-family:'Calistoga',Georgia,serif;color:#FFFFFF;margin:0 0 0.65rem 0;letter-spacing:-0.01em;">Active College Node Required</div>
    <div style="color:#94A3B8;margin:0;font-family:'Inter',sans-serif;font-size:0.95rem;">Select an institution node to begin query search, or select General for universal Indian college guidelines.</div>
</div>
""", unsafe_allow_html=True)
        
        c_names = [c["name"] for c in COLLEGES]
        selected_name = st.selectbox("Quick Select Institution Node", ["-- Select Institution --"] + c_names)
        if selected_name != "-- Select Institution --":
            selected_c = next(c for c in COLLEGES if c["name"] == selected_name)
            st.session_state.selected_college = selected_c["id"]
            st.session_state.messages = []
            st.rerun()
            
        st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
        if st.button("Browse All Colleges in Overview 🏛", use_container_width=True):
            st.session_state.page = "🏠 Overview"
            st.rerun()


    st.markdown(f"""
<div style="background-color:#0F172A;background-image:radial-gradient(rgba(255,255,255,0.04) 1px,transparent 1px);background-size:24px 24px;border:1px solid #1E293B;border-radius:16px;padding:2.25rem;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin-bottom:1.5rem;">
    <div style="display:inline-flex;align-items:center;gap:0.6rem;border:1px solid rgba(0,82,255,0.35);background:rgba(0,82,255,0.08);border-radius:9999px;padding:0.3rem 1rem;margin-bottom:1rem;">
        <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#0052FF;box-shadow:0 0 6px #0052FF;"></span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.15em;color:#60a5fa;">Active Node</span>
    </div>
    <div style="font-size:1.85rem;font-weight:400;font-family:'Calistoga',Georgia,serif;color:#FFFFFF;margin:0 0 0.5rem 0;letter-spacing:-0.01em;">{active_c.get('name','CampusAI')}</div>
    <div style="color:#94A3B8;margin:0 0 1.1rem 0;font-family:'Inter',sans-serif;font-size:0.92rem;">Query statistics, admissions, placement logs, and calendar schedules directly from the verified database.</div>
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
        <span style="display:inline-flex;align-items:center;padding:0.2rem 0.55rem;background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.3);border-radius:4px;font-size:0.68rem;font-weight:500;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">🤖 GEMINI 2.0 FLASH</span>
        <span style="display:inline-flex;align-items:center;padding:0.2rem 0.55rem;background:rgba(0,82,255,0.15);color:#60a5fa;border:1px solid rgba(0,82,255,0.3);border-radius:4px;font-size:0.68rem;font-weight:500;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">📚 {get_vector_store_docs_count()} KNOWLEDGE CHUNKS</span>
        <span style="display:inline-flex;align-items:center;padding:0.2rem 0.55rem;background:#10b981;color:#ffffff;border:1px solid #10b981;border-radius:4px;font-size:0.68rem;font-weight:500;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">⚡ REAL-TIME RAG</span>
    </div>
</div>
""", unsafe_allow_html=True)

    if st.session_state.selected_college != "general":
        tags_html = " ".join([f'<span class="college-tag">{t}</span>' for t in active_c.get('tags', [])])
        st.markdown(f"""
        <div class="active-college-info" style="background:var(--bg-surface);border:1px solid var(--border);padding:1.25rem;border-radius:8px;margin-bottom:1.5rem;font-size:0.88rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;flex-wrap:wrap;gap:0.5rem;">
                <span style="font-weight:600;color:var(--text-primary);">📍 Location: <span style="font-weight:normal;color:var(--text-secondary);">{active_c.get('location')}</span></span>
                <span style="font-weight:600;color:var(--text-primary);">🏛️ Type: <span style="font-weight:normal;color:var(--text-secondary);">{active_c.get('type')}</span></span>
            </div>
            <div style="color:var(--text-secondary);line-height:1.5;margin-bottom:0.75rem;">
                {active_c.get('desc')}
            </div>
            <div style="display:flex;gap:0.35rem;flex-wrap:wrap;">
                {tags_html}
            </div>
        </div>
        """, unsafe_allow_html=True)


    # College-specific quick suggestion chips
    college_suggestions = {
        "general":  ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "📚 Library timings", "📝 Bonafide certificate", "🎓 CGPA calculation", "🔬 Technical clubs"],
        "iith":     ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "📐 Fractal Academics model", "💰 IITH fee structure", "🚌 Bus timing from Nagole", "🎓 MCM scholarship"],
        "iiith":    ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💻 Ada cluster specs", "🍽️ Kadamba dining menu", "🏠 Hostel allocation policy", "📝 UGEE exam details"],
        "nalsar":   ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "📋 CLAT cutoff rank", "💰 NALSAR fee structure", "⚖️ LLB programs offered", "🏛️ Law school facilities"],
        "nims":     ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "🩺 NEET PG cutoff by category", "📋 MD/MS admission", "💰 DNB program fee", "🏥 BPT eligibility"],
        "hcu":      ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "🏠 50 km hostel rule", "📱 Samarth portal process", "💰 Hostel fee SC/ST", "📝 GRE requirements"],
        "osmania":  ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "📊 SGPA CGPA formula", "📝 Internal exam format", "✅ Attendance requirement", "📋 CBCS credit system"],
        "bits_hyd": ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "🛒 Campus shops list", "🏥 Medical center timings", "🏦 SBI branch on campus", "💊 Pharmacy details"],
        "isb_hyd":  ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💼 ISB average package", "💰 ISB PGP program fee", "📋 ISB GMAT score required", "💼 Consulting recruiters at ISB"],
        "imt_hyd":  ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "📈 IMT PGDM fees", "💰 EWS scholarship at IMT", "👧 Female diversity fee refund", "💼 IMT placement statistics"],
        "ibs_hyd":  ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "📊 IBS average placement CTC", "📖 Case study research center", "📋 IBSAT exam cutoff", "💰 IBS total MBA fees"],
        "omc":      ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "🩺 OMC service bond penalty", "💰 OMC MBBS annual tuition fee", "🏥 OMC specialized teaching hospitals", "🩺 NEET PG general cutoff rank"],
        "nizam":    ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "🏛️ Nizam College B.Sc Data Science fee", "💰 Nizam regular vs self-financed fees", "📋 Nizam DOST admission process", "💼 Nizam placement cell TASK"],
        "st_francis":["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "👩‍🎓 St. Francis placement packages", "💰 St. Francis BMS fee", "📋 St. Francis online admission criteria", "⛪ St. Francis minority seat reservation"],
        "jntuh":    ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💰 JNTUH fee range", "📋 JNTUH admission exams", "💼 JNTUH average placement CTC", "🔬 JNTUH B.Tech programs"],
        "cbit":     ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💰 CBIT total B.Tech fee", "💼 CBIT highest placement package", "📋 CBIT TS EAMCET cutoffs", "💼 CBIT average CSE CTC"],
        "griet":    ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💰 GRIET tuition fees", "💼 GRIET average placement package", "📋 GRIET B.Tech seat intake", "💼 GRIET highest CTC recruiters"],
        "vnr_vjiet": ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💰 VNR VJIET B.Tech fees", "💼 VNR VJIET median package", "📋 VNR VJIET total intake", "💼 VNR VJIET top corporate recruiters"],
        "vardhaman":["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💰 Vardhaman College fees", "💼 Vardhaman median package", "📋 Vardhaman CSE average CTC", "🔬 Vardhaman major admission exams"],
        "anurag":   ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💰 Anurag University fee range", "📋 Anurag admission exams", "💼 Anurag average package", "🔬 Anurag B.Tech intake"],
        "iare":     ["💼 Compare placements", "🎓 Scholarship details", "🏠 Hostel facilities", "📋 Admission cutoffs", "💰 IARE tuition fees", "💼 IARE average CSE CTC", "💼 IARE highest placement package", "📋 IARE TS EAMCET criteria"],
    }
    suggestions = college_suggestions.get(st.session_state.selected_college, college_suggestions["general"])

    if not st.session_state.messages:
        st.markdown(f"""
        <div style="font-size:0.75rem;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.05em;margin-top:1.5rem;margin-bottom:0.75rem;">
            🔥 MOST ASKED ABOUT {active_c.get('short','').upper()}
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(4)
        for i, sug in enumerate(suggestions):
            # Strip leading emoji+space safely to get clean query text
            parts = sug.split(" ", 1)
            query_text = parts[1].strip() if len(parts) > 1 else sug
            display_label = query_text.upper()
            if cols[i % 4].button(display_label, key=f"sug_{i}", use_container_width=True):
                send_message(query_text)
                st.rerun()

        st.divider()

    # Welcome / empty state
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="empty-state">
            <span class="empty-state-icon">{active_c.get('icon','👋')}</span>
            <div class="empty-state-title">Ready to help with {active_c.get('short', 'your college')}!</div>
            <div class="empty-state-desc">
                Ask me about <strong>fees, placements, admissions, hostel rules, scholarships,
                bus routes, clubs</strong> or anything else about
                <strong>{active_c.get('name','')}</strong>.
                I'll retrieve exact data from the knowledge base.
            </div>
        </div>
        """, unsafe_allow_html=True)




    # Chat messages
    chat_area = st.container()
    with chat_area:
        for idx, msg in enumerate(st.session_state.messages):
            render_message(msg, idx)
        # Auto-scroll to the bottom after rendering messages
        if st.session_state.messages:
            st.markdown(
                '<div id="chat-bottom"></div>'
                '<script>document.getElementById("chat-bottom").scrollIntoView({behavior:"smooth"});</script>',
                unsafe_allow_html=True
            )

    # Quick Actions Row
    st.markdown(f"""
    <div style="font-size:0.65rem;font-weight:700;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.12em;margin-top:1.5rem;margin-bottom:0.6rem; font-family:'JetBrains Mono',monospace">
        ⚡ Quick Actions
    </div>
    """, unsafe_allow_html=True)
    
    qa_cols = st.columns(5)
    actions = [
        ("💼 Placements", "What are the latest placement records, highest package, average package and top recruiters?"),
        ("🏠 Hostel", "Tell me about the hostel rooms, facilities, mess fees and hostel rules."),
        ("🎓 Scholarships", "What scholarships, fee waivers and financial aid options are available?"),
        ("📋 Cutoffs", "What are the cutoff ranks and admission eligibility criteria?"),
        ("📞 Faculty", "Show me the faculty directory, department HODs and office contact details.")
    ]
    for col_idx, (label, query_text) in enumerate(actions):
        if qa_cols[col_idx].button(label, key=f"qa_{col_idx}", use_container_width=True):
            send_message(query_text)
            st.rerun()

    st.markdown("<div style='margin-bottom:0.75rem'></div>", unsafe_allow_html=True)

    # Input area — single unified input with Enter-to-submit via form
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([6, 1])
        with col_input:
            user_input = st.text_input(
                "Message",
                placeholder="Type your question here (e.g. library timings, placement statistics)...",
                label_visibility="collapsed",
                key="chat_input"
            )
        with col_send:
            send_btn = st.form_submit_button("Send 🚀", use_container_width=True)

        if send_btn and user_input and user_input.strip():
            send_message(user_input.strip())
            st.rerun()

    # Response stats
    if st.session_state.messages:
        bot_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]
        if bot_msgs:
            avg_time = sum(m.get("response_time_ms", 0) for m in bot_msgs) / len(bot_msgs)
            st.caption(f"💬 {len(bot_msgs)} responses | ⚡ Avg: {avg_time:.0f}ms")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
# ==============================================================================
# PAGE: DASHBOARD
# ==============================================================================
if st.session_state.page == "📊 Dashboard":
    active_college_id = st.session_state.get("selected_college") or "general"
    active_c = COLLEGE_MAP.get(active_college_id, {})

    st.markdown(f"""
    <div class="campus-header" style="background-color: #0F172A !important; background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important; background-size: 24px 24px !important; color: #F8FAFC !important; border-color: #1E293B !important; padding: 2.25rem !important; border-radius: 16px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;">
        <div class="section-label-badge">
            <span class="section-label-dot"></span>
            <span class="section-label-text">{active_c.get('short','CampusAI')}</span>
        </div>
        <h1 style="font-size:2.0rem;font-weight:400;font-family:'Calistoga',serif !important;color:#FFFFFF !important;margin:0 0 0.75rem 0;letter-spacing:-0.01em;">Campus Intelligence Dashboard</h1>
        <p style="color:#94A3B8 !important;margin:0;">Comprehensive overview of campus information categories and quick access resources.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats Row ──────────────────────────────────────────────────────────────
    try:
        from core.database import get_analytics_summary
        stats = get_analytics_summary()
        s_total = stats.get("total_queries", 0)
        s_today = stats.get("today_queries", 0)
        s_sat = stats.get("satisfaction_rate", 0)
        s_rt = stats.get("avg_response_time_ms", 0)
    except Exception:
        s_total = s_today = s_sat = s_rt = 0

    m1, m2, m3, m4 = st.columns(4)
    for col, val, label, icon in [
        (m1, s_total, "Total Queries", "💬"),
        (m2, s_today, "Today's Queries", "📅"),
        (m3, f"{s_sat}%", "Satisfaction Rate", "⭐"),
        (m4, f"{int(s_rt)}ms", "Avg Response", "⚡"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div style="font-size:1.5rem">{icon}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">🔥 Live Student Trends & Inquiries</div>', unsafe_allow_html=True)

    col_dash1, col_dash2 = st.columns(2)
    with col_dash1:
        st.markdown(f"""
        <div class="contact-card" style="margin-bottom:1.5rem; border-left: 3px solid var(--accent);">
            <div style="font-weight:600;font-size:1.1rem;color:var(--text-primary);margin-bottom:0.75rem;">🔥 Trending College Nodes This Week</div>
            <div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);">
                1. <strong>IIT Hyderabad</strong> — 42% increase in placement eligibility inquiries.<br>
                2. <strong>BITS Hyderabad</strong> — High volume of hostel facilities queries.<br>
                3. <strong>NALSAR Law</strong> — CLAT cutoff searches ahead of counseling.
            </div>
        </div>
        <div class="contact-card" style="margin-bottom:1.5rem; border-left: 3px solid var(--accent);">
            <div style="font-weight:600;font-size:1.1rem;color:var(--text-primary);margin-bottom:0.75rem;">💎 Most Popular Scholarships</div>
            <div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);">
                • <strong>MCM Scholarship</strong> (IIT Hyderabad) — Full tuition waivers.<br>
                • <strong>Ishan Uday Scheme</strong> (NALSAR) — UGC North-East scheme.<br>
                • <strong>EWS PGDM Concessions</strong> (IMT) — 95% waiver query peak.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_dash2:
        st.markdown("""
        <div class="contact-card" style="margin-bottom:1.5rem; border-left: 3px solid var(--accent-sec);">
            <div style="font-weight:600;font-size:1.1rem;color:var(--text-primary);margin-bottom:0.75rem;">📊 Query Volume by Category</div>
            <div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);">
                📈 <strong>Placement Packages</strong> — 40% of all inquiries.<br>
                📋 <strong>Admissions & Eligibility</strong> — 25% query load.<br>
                🏠 <strong>Hostels & Mess rules</strong> — 20% active volume.<br>
                🤝 <strong>Student Clubs & NSS</strong> — 15% curiosity rate.
            </div>
        </div>
        <div class="contact-card" style="margin-bottom:1.5rem; border-left: 3px solid var(--accent-sec);">
            <div style="font-weight:600;font-size:1.1rem;color:var(--text-primary);margin-bottom:0.75rem;">🎯 Top Student Search Inquiries</div>
            <div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);">
                • "What is the highest package at IIIT-H?"<br>
                • "How is attendance calculated in Osmania?"<br>
                • "Is there a service bond penalty in OMC?"
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick Access Cards ─────────────────────────────────────────────────────
    st.markdown('<div class="section-title">CAMPUS INFORMATION CATEGORIES</div>', unsafe_allow_html=True)

    categories = [
        ("🎓", "Academics", "CGPA, exams, attendance, grading, backlogs, CBCS system"),
        ("🏠", "Hostel & Accommodation", "Hostel rules, facilities, mess timings, warden contact"),
        ("📚", "Library Services", "Book lending, N-LIST access, digital resources, timings"),
        ("💼", "Placement & Careers", "Campus drives, internships, resume tips, salary packages"),
        ("🎭", "Clubs & Activities", "Technical, cultural, sports, NSS, NCC, student council"),
        ("🏥", "Health & Medical", "Health center, mental health, emergency contacts"),
        ("📋", "Documents & Certificates", "Bonafide, TC, migration, transcript, no dues"),
        ("💰", "Scholarships & Fees", "NSP, central/state schemes, fee payment, concessions"),
        ("🚌", "Transport & Facilities", "Bus routes, WiFi, canteen, sports, bank/ATM on campus"),
        ("🔬", "Research & Innovation", "R&D cell, patents, paper publication, conferences"),
        ("🏫", "College Types", "Engineering, Medical, Arts, Management, Law, Architecture"),
        ("🌐", "Higher Education", "GATE, GRE, CAT, IELTS, study abroad guidance"),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(categories):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">{get_college_icon_html(icon, size=24)}</div>
                <div class="info-card-title">{title}</div>
                <div class="info-card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── College Types Reference ────────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="section-title">INDIAN HIGHER EDUCATION LANDSCAPE</div>', unsafe_allow_html=True)

    college_data = {
        "Type": ["Engineering", "Medical", "Arts & Science", "Management", "Law", "Architecture", "Agriculture", "Pharmacy"],
        "Programs": ["B.Tech, M.Tech", "MBBS, BDS, BPT", "BA, BSc, BCom", "MBA, BBA, PGDM", "LLB, BA LLB", "B.Arch, M.Arch", "BSc Agri, BVSc", "B.Pharm, M.Pharm"],
        "Entrance Exam": ["JEE/State CETs", "NEET", "CUET/Merit", "CAT/MAT/XAT", "CLAT/AILET", "NATA/JEE-2", "ICAR AIEEA", "State Pharm CET"],
        "Regulatory Body": ["AICTE", "NMC/DCI", "UGC", "AICTE/UGC", "BCI", "COA", "ICAR", "PCI"],
        "Duration": ["4 yrs (UG)", "5.5 yrs", "3 yrs (UG)", "2 yrs (PG)", "3-5 yrs", "5 yrs", "4 yrs", "4 yrs (B.Pharm)"],
    }

    df = pd.DataFrame(college_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    # ── Common Questions ───────────────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="section-title">FREQUENTLY ASKED QUESTIONS</div>', unsafe_allow_html=True)

    faqs = [
        ("What is minimum attendance required?", "📝 Most colleges require **75% minimum attendance**. Some (IITs, medical colleges) require **85%**. Students below 65% may be detained."),
        ("How is CGPA calculated?", "📊 CGPA = Sum(Grade Points × Credits) / Total Credits. Most universities use a 10-point scale where O=10, A+=9, A=8, B+=7, B=6, C=5, P=4."),
        ("How do I get a bonafide certificate?", "📋 Apply at the college office with your ID card and a small fee (Rs. 20-50). Issued within 2-3 working days. Required for bank loans, internships, railway concession."),
        ("What is NSS and how to join?", "🤝 NSS (National Service Scheme) is a Central Govt. program for 240 hours of community service. Register at the beginning of the academic year through your college's NSS unit."),
    ]

    for q, a in faqs:
        with st.expander(f"💬 {q}"):
            st.markdown(a)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EVENTS
# ══════════════════════════════════════════════════════════════════════════════
# ==============================================================================
# PAGE: EVENTS
# ==============================================================================
if st.session_state.page == "📅 Events":
    active_college_id = st.session_state.get("selected_college") or "general"
    active_c = COLLEGE_MAP.get(active_college_id, {})

    st.markdown(f"""
    <div class="campus-header" style="background-color: #0F172A !important; background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important; background-size: 24px 24px !important; color: #F8FAFC !important; border-color: #1E293B !important; padding: 2.25rem !important; border-radius: 16px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;">
        <div class="section-label-badge">
            <span class="section-label-dot"></span>
            <span class="section-label-text">{active_c.get('short','CampusAI')}</span>
        </div>
        <h1 style="font-size:2.0rem;font-weight:400;font-family:'Calistoga',serif !important;color:#FFFFFF !important;margin:0 0 0.75rem 0;letter-spacing:-0.01em;">Academic Calendar & Events</h1>
        <p style="color:#94A3B8 !important;margin:0;">Complete academic year schedule — exams, fests, sports, holidays, and important deadlines.</p>
    </div>
    """, unsafe_allow_html=True)

    all_events = load_events()

    # Filter controls
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All", "Exam", "Cultural", "Technical", "Sports", "Holiday", "Academic", "Placement", "Social", "Orientation"],
            index=0
        )
    with col2:
        semester_filter = st.selectbox(
            "Filter by Semester",
            ["All Semesters", "Odd Semester", "Even Semester"],
            index=0
        )
    with col3:
        show_upcoming = st.checkbox("Show Upcoming Only", value=False)

    # Apply filters
    filtered = all_events
    today_str = date.today().isoformat()

    if category_filter != "All":
        filtered = [e for e in filtered if (e.get("category") or "").lower() == category_filter.lower()]
    if semester_filter != "All Semesters":
        key = "odd" if "Odd" in semester_filter else "even"
        filtered = [e for e in filtered if key in (e.get("semester") or "").lower()]
    if show_upcoming:
        filtered = [e for e in filtered if (e.get("date") or "") >= today_str]

    st.caption(f"Showing {len(filtered)} events")
    st.divider()

    # Category badge colors
    badge_map = {
        "exam": "badge-exam",
        "cultural": "badge-cultural",
        "sports": "badge-sports",
        "holiday": "badge-holiday",
        "academic": "badge-academic",
        "placement": "badge-placement",
        "technical": "badge-academic",
        "social": "badge-cultural",
        "orientation": "badge-academic",
    }

    if not filtered:
        st.info("No events found for the selected filters.")
    else:
        # Group by month
        from itertools import groupby
        def get_month(ev):
            d = ev.get("date", "")
            if len(d) >= 7:
                try:
                    return datetime.strptime(d[:7], "%Y-%m").strftime("%B %Y")
                except Exception:
                    pass
            return "TBA"

        grouped = {}
        for ev in filtered:
            month = get_month(ev)
            grouped.setdefault(month, []).append(ev)

        for month, events in grouped.items():
            st.markdown(f"**{month.upper()}**")
            for ev in events:
                cat = (ev.get("category") or "academic").lower()
                badge_class = badge_map.get(cat, "badge-academic")
                is_past = ev.get("date", "") < today_str
                opacity = "0.5" if is_past else "1"

                st.markdown(f"""
                <div class="contact-card" style="margin-bottom:0.5rem;opacity:{opacity}">
                    <div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap">
                        <div style="font-weight:600;color:var(--text-primary)">{ev.get('event','Event')}</div>
                        <span class="event-badge {badge_class}">{cat}</span>
                        {'<span class="event-badge badge-past">Past</span>' if is_past else ''}
                    </div>
                    <div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.3rem">
                        📅 {ev.get('date','TBA')} &nbsp;|&nbsp; {(ev.get('semester') or '').split('(')[0].strip()}
                    </div>
                    <div style="font-size:0.85rem;color:var(--text-secondary);margin-top:0.4rem">{ev.get('description','')}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    # Important Deadlines section
    st.divider()
    st.markdown('<div class="section-title">IMPORTANT ANNUAL DEADLINES</div>', unsafe_allow_html=True)

    try:
        cal_file = DATA_DIR / "events" / "academic_calendar.json"
        with open(cal_file, "r", encoding="utf-8") as f:
            cal_data = json.load(f)
        deadlines = cal_data.get("important_deadlines", [])

        dl_cols = st.columns(2)
        for i, dl in enumerate(deadlines):
            with dl_cols[i % 2]:
                st.markdown(f"""
                <div class="contact-card" style="margin-bottom:0.5rem">
                    <div style="font-weight:600;color:var(--accent)">📌 {dl.get('deadline','')}</div>
                    <div style="font-size:0.85rem;color:var(--text-secondary);margin-top:0.3rem">{dl.get('description','')}</div>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading deadlines: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CONTACTS
# ══════════════════════════════════════════════════════════════════════════════
# ==============================================================================
# PAGE: CONTACTS
# ==============================================================================
if st.session_state.page == "📞 Contacts":
    active_college_id = st.session_state.get("selected_college") or "general"
    active_c = COLLEGE_MAP.get(active_college_id, {})

    st.markdown(f"""
    <div class="campus-header" style="background-color: #0F172A !important; background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important; background-size: 24px 24px !important; color: #F8FAFC !important; border-color: #1E293B !important; padding: 2.25rem !important; border-radius: 16px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;">
        <div class="section-label-badge">
            <span class="section-label-dot"></span>
            <span class="section-label-text">{active_c.get('short','CampusAI')}</span>
        </div>
        <h1 style="font-size:2.0rem;font-weight:400;font-family:'Calistoga',serif !important;color:#FFFFFF !important;margin:0 0 0.75rem 0;letter-spacing:-0.01em;">Faculty & Staff Directory</h1>
        <p style="color:#94A3B8 !important;margin:0;">Search for any faculty, HOD, warden, or administrative contact across all departments.</p>
    </div>
    """, unsafe_allow_html=True)

    contacts = load_contacts()

    if not contacts:
        st.error("Contact directory not found. Check `data/contacts/directory.csv`")
    else:
        # Search and filter
        col1, col2 = st.columns([3, 2])
        with col1:
            search_term = st.text_input(
                "Search",
                placeholder="🔍  Search by name, department, designation, or specialization...",
                label_visibility="collapsed"
            )
        with col2:
            departments = sorted(set(c.get("department", "") for c in contacts))
            dept_filter = st.selectbox("Department", ["All Departments"] + departments, label_visibility="collapsed")

        # Apply filters
        filtered_contacts = contacts
        if search_term:
            st_lower = search_term.lower()
            filtered_contacts = [
                c for c in filtered_contacts
                if any(st_lower in str(c.get(f, "")).lower()
                       for f in ["name", "designation", "department", "specialization"])
            ]
        if dept_filter != "All Departments":
            filtered_contacts = [c for c in filtered_contacts if c.get("department") == dept_filter]

        st.caption(f"Found {len(filtered_contacts)} contacts")
        st.divider()

        if not filtered_contacts:
            st.info("No contacts found. Try a different search term.")
        else:
            # Display contacts in cards
            cols = st.columns(2)
            for i, contact in enumerate(filtered_contacts):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="contact-card" style="margin-bottom:1rem">
                        <div style="display:flex;align-items:center;gap:0.75rem">
                            <div style="width:40px;height:40px;border-radius:50% !important;
                                        border:1px solid var(--border);
                                        background-color:rgba(99,102,241,0.1);color:var(--accent);
                                        display:flex;align-items:center;justify-content:center;
                                        font-size:1.1rem;flex-shrink:0">👤</div>
                            <div>
                                <div class="contact-name">{contact.get('name','N/A')}</div>
                                <div class="contact-role">{contact.get('designation','')}</div>
                                <div class="contact-dept">{contact.get('department','')}</div>
                            </div>
                        </div>
                        <div style="height:1px;background:var(--border);margin:0.75rem 0"></div>
                        <div class="contact-info">
                            📧 <a href="mailto:{contact.get('email','')}" style="color:#4f8ef7;text-decoration:none">{contact.get('email','N/A')}</a><br>
                            📞 {contact.get('phone','N/A')}<br>
                            🏢 {contact.get('office_location','N/A')}<br>
                            🕐 {contact.get('office_hours','N/A')}
                        </div>
                        {f'<div style="margin-top:0.5rem;font-size:0.75rem;color:var(--text-muted)">🔬 {contact.get("specialization","")}</div>' if contact.get('specialization') else ''}
                    </div>
                    """, unsafe_allow_html=True)

        # Download contacts
        st.divider()
        df_contacts = pd.DataFrame(filtered_contacts)
        csv_data = df_contacts.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Contact List (CSV)",
            data=csv_data,
            file_name="campus_contacts.csv",
            mime="text/csv"
        )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
# ==============================================================================
# PAGE: ANALYTICS
# ==============================================================================
if st.session_state.page == "📈 Insights":
    active_college_id = st.session_state.get("selected_college") or "general"
    active_c = COLLEGE_MAP.get(active_college_id, {})

    st.markdown(f"""
    <div class="campus-header" style="background-color: #0F172A !important; background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important; background-size: 24px 24px !important; color: #F8FAFC !important; border-color: #1E293B !important; padding: 2.25rem !important; border-radius: 16px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;">
        <div class="section-label-badge">
            <span class="section-label-dot"></span>
            <span class="section-label-text">{active_c.get('short','CampusAI')}</span>
        </div>
        <h1 style="font-size:2.0rem;font-weight:400;font-family:'Calistoga',serif !important;color:#FFFFFF !important;margin:0 0 0.75rem 0;letter-spacing:-0.01em;">System Analytics & Usage</h1>
        <p style="color:#94A3B8 !important;margin:0;">Usage statistics, popular queries, and performance metrics for CampusAI.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        from core.database import get_analytics_summary, get_recent_queries, get_popular_queries
        stats = get_analytics_summary()
        recent = get_recent_queries(limit=10)
        popular = get_popular_queries(limit=8)
    except Exception as e:
        st.error(f"Analytics unavailable: {e}")
        st.stop()

    # ── Summary Metrics ────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        (c1, stats.get("total_queries", 0), "Total Queries", "💬"),
        (c2, stats.get("today_queries", 0), "Today", "📅"),
        (c3, stats.get("positive_feedback", 0), "👍 Helpful", "✅"),
        (c4, stats.get("negative_feedback", 0), "👎 Not Helpful", "❌"),
        (c5, f"{stats.get('satisfaction_rate', 0)}%", "Satisfaction", "⭐"),
    ]
    for col, val, label, icon in metrics:
        col.markdown(f"""
        <div class="metric-card">
            <div style="font-size:1.2rem">{icon}</div>
            <div class="metric-value" style="font-size:1.5rem">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ─────────────────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    # Dynamic styling colors for Plotly charts
    dark_mode = st.session_state.get("dark_mode", False)
    plotly_template = "plotly_dark" if dark_mode else "plotly_white"
    plotly_text = "#f0f4ff" if dark_mode else "#475569"
    plotly_grid = "rgba(255,255,255,0.08)" if dark_mode else "#f1f5f9"

    with col_left:
        st.markdown('<div class="section-title">QUERIES PER DAY (LAST 7 DAYS)</div>', unsafe_allow_html=True)
        daily = stats.get("daily_counts", [])
        if daily:
            df_daily = pd.DataFrame(daily)
            fig = px.bar(
                df_daily, x="day", y="count",
                color_discrete_sequence=["#6366f1"],
                template=plotly_template
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                font=dict(color=plotly_text, family="Outfit"),
                xaxis_title="",
                yaxis_title="Queries"
            )
            fig.update_xaxes(showgrid=False, color=plotly_text, linecolor=plotly_grid)
            fig.update_yaxes(showgrid=True, gridcolor=plotly_grid, color=plotly_text, linecolor=plotly_grid)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No query data yet. Start chatting to see analytics!")

    with col_right:
        st.markdown('<div class="section-title">QUERIES BY CATEGORY</div>', unsafe_allow_html=True)
        top_cats = stats.get("top_categories", [])
        if top_cats:
            df_cats = pd.DataFrame(top_cats)
            colors = ["#6366f1", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b"]
            fig2 = px.pie(
                df_cats, names="category", values="count",
                color_discrete_sequence=colors,
                template=plotly_template,
                hole=0.45
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(color=plotly_text, family="Outfit"),
                legend=dict(font=dict(color=plotly_text))
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No category data yet.")

    # ── Popular Queries ────────────────────────────────────────────────────────
    st.divider()
    col_pop, col_recent = st.columns(2)

    with col_pop:
        st.markdown('<div class="section-title">POPULAR QUERIES</div>', unsafe_allow_html=True)
        if popular:
            for i, pq in enumerate(popular):
                freq = pq.get("frequency", 1)
                query_text = pq.get("user_query", "")[:60]
                bar_width = int((freq / max(p.get("frequency", 1) for p in popular)) * 100)
                st.markdown(f"""
                <div style="margin-bottom:0.75rem">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.2rem">
                        <span style="font-size:0.85rem;color:var(--text-primary)">{i+1}. {query_text}</span>
                        <span style="font-size:0.75rem;color:var(--accent);font-weight:600">{freq}x</span>
                    </div>
                    <div style="background:var(--border);height:6px;border-radius:3px !important;overflow:hidden;">
                        <div style="background:var(--accent);width:{bar_width}%;height:100%;border-radius:3px !important;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No popular queries yet.")

    with col_recent:
        st.markdown('<div class="section-title">RECENT QUERIES</div>', unsafe_allow_html=True)
        if recent:
            for q in recent[:8]:
                timestamp = (q.get("timestamp") or "")[:16].replace("T", " ")
                category = q.get("category", "general")
                badge_class = {
                    "academic": "badge-academic",
                    "facility": "badge-sports",
                    "placement": "badge-placement",
                    "clubs": "badge-cultural",
                    "contact": "badge-exam",
                }.get(category, "badge-academic")

                st.markdown(f"""
                <div class="contact-card" style="margin-bottom:0.5rem">
                    <div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap">
                        <span style="font-size:0.85rem;color:var(--text-primary)">{q.get('user_query','')[:60]}{('...' if len(q.get('user_query','')) > 60 else '')}</span>
                        <span class="event-badge {badge_class}">{category}</span>
                    </div>
                    <div style="font-size:0.72rem;color:var(--text-muted);margin-top:0.3rem">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent queries. Start chatting!")

    # Performance
    st.divider()
    avg_rt = stats.get("avg_response_time_ms", 0)
    st.markdown(f"""
    <div style="text-align:center;padding:1.25rem;color:var(--text-secondary);font-size:0.85rem;
                background:var(--bg-surface);border:2px solid var(--border)">
        ⚡ Avg Response: <strong style="color:var(--accent)">{int(avg_rt)}ms</strong> &nbsp;·&nbsp;
        🤖 Model: <strong style="color:var(--accent)">gemini-2.0-flash</strong> &nbsp;·&nbsp;
        💾 Session: <strong style="color:var(--accent);font-family:'JetBrains Mono',monospace">{st.session_state.session_id[:8]}...</strong>
    </div>
    """, unsafe_allow_html=True)




