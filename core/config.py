"""
config.py — Single source of truth for all shared configuration.
Paths, college registry, API key validation, and constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", str(ROOT / "vector_store")))
DB_PATH = os.getenv("DB_PATH", str(ROOT / "campus.db"))

# ── Load .env once at import time ─────────────────────────────────────────────
load_dotenv(ROOT / ".env")

# ── API Key Validation ────────────────────────────────────────────────────────
PLACEHOLDER_KEYS = {
    "your_openai_api_key_here",
    "your_google_gemini_api_key_here",
}


def _is_valid_key(key: str) -> bool:
    return bool(key and key.strip() and key.strip() not in PLACEHOLDER_KEYS)


def is_openai_configured() -> bool:
    return _is_valid_key(os.getenv("OPENAI_API_KEY", ""))


def is_google_configured() -> bool:
    return _is_valid_key(os.getenv("GOOGLE_API_KEY", ""))


def is_any_api_configured() -> bool:
    return is_openai_configured() or is_google_configured()


def get_active_provider() -> str:
    """Return 'openai' or 'gemini' based on available keys and LLM_PROVIDER env."""
    provider = os.getenv("LLM_PROVIDER", "").lower().strip()
    if provider:
        return provider
    if is_openai_configured():
        return "openai"
    if is_google_configured():
        return "gemini"
    return "openai"


# ── College Registry (Canonical Source) ───────────────────────────────────────
COLLEGES = [
    {
        "id": "general",
        "name": "General (All Indian Colleges)",
        "short": "General",
        "icon": "\U0001f1ee\U0001f1f3",
        "type": "Universal Guidelines",
        "location": "Pan-India",
        "color": "#4f8ef7",
        "desc": "Generic queries about any Indian college \u2014 attendance, CGPA, hostels, admissions, clubs, procedures.",
        "tags": ["Attendance", "CGPA", "Hostel", "Clubs", "Procedures"],
        "ranking": "Top 100 Overall",
        "students": "100k+ Active",
        "placement": "Multi-sector",
    },
    {
        "id": "iith",
        "name": "IIT Hyderabad (IITH)",
        "short": "IITH",
        "icon": "\U0001f52c",
        "type": "Central Government Institute",
        "location": "Kandi, Hyderabad",
        "color": "#f0883e",
        "desc": "Fractal Academics model, JEE admissions, fees, MCM scholarship, placements (\u20b990L highest), bus routes.",
        "tags": ["Fractal Academics", "JEE", "Scholarships", "Placements", "Bus Routes"],
        "ranking": "NIRF Eng #8",
        "students": "4,200+ Students",
        "placement": "\u20b990L Highest Package",
    },
    {
        "id": "iiith",
        "name": "IIIT Hyderabad (IIITH)",
        "short": "IIITH",
        "icon": "\U0001f4bb",
        "type": "Autonomous Deemed University (PPP)",
        "location": "Gachibowli, Hyderabad",
        "color": "#39c5b9",
        "desc": "Ada supercomputer (70 TFLOPS), UGEE/JEE admissions, 3 dining halls, placements (\u20b9128L highest, \u20b933.96L avg).",
        "tags": ["Supercomputer", "UGEE", "Dining", "Placements", "Hostels"],
        "ranking": "NIRF Eng #55",
        "students": "2,100+ Students",
        "placement": "\u20b91.28Cr Highest / \u20b933.96L Avg",
    },
    {
        "id": "nalsar",
        "name": "NALSAR University of Law",
        "short": "NALSAR",
        "icon": "\u2696\ufe0f",
        "type": "National Law University",
        "location": "Hyderabad",
        "color": "#7c5cbf",
        "desc": "CLAT cutoff (Rank 1\u2013130), fee structure (\u20b93.17L/yr), Ishan Uday & Indira Gandhi scholarships.",
        "tags": ["CLAT", "Law", "Scholarships", "Fees", "Admissions"],
        "ranking": "NIRF Law #3",
        "students": "1,200+ Students",
        "placement": "\u20b922L Avg Package",
    },
    {
        "id": "nims",
        "name": "NIMS \u2014 Nizam\u2019s Institute of Medical Sciences",
        "short": "NIMS",
        "icon": "\U0001f3e5",
        "type": "Autonomous Medical University",
        "location": "Hyderabad",
        "color": "#3fb950",
        "desc": "MD/MS/DM/DNB/BPT programs, NEET PG cutoffs by category, NIMSET exam, fee ranges.",
        "tags": ["NEET PG", "MD", "MS", "DNB", "Cutoffs"],
        "ranking": "NIRF Medical #13",
        "students": "1,800+ Students",
        "placement": "Clinical Residencies",
    },
    {
        "id": "hcu",
        "name": "University of Hyderabad (HCU)",
        "short": "HCU",
        "icon": "\U0001f393",
        "type": "Central University",
        "location": "Gachibowli, Hyderabad",
        "color": "#d29922",
        "desc": "2,300-acre campus, 23 hostels, Samarth portal, 50 km radius hostel rule, GRE/IELTS requirements.",
        "tags": ["Hostel", "Samarth Portal", "50km Rule", "GRE", "IELTS"],
        "ranking": "NIRF University #10",
        "students": "6,500+ Students",
        "placement": "Public R&D Placements",
    },
    {
        "id": "osmania",
        "name": "Osmania University",
        "short": "OU",
        "icon": "\U0001f4dc",
        "type": "State University",
        "location": "Hyderabad",
        "color": "#e3b341",
        "desc": "CBCS rules, SGPA/CGPA formulas, 75% attendance, 20% internal assessment, dual examiner system.",
        "tags": ["CBCS", "SGPA", "CGPA", "Attendance", "Internal Marks"],
        "ranking": "NIRF University #36",
        "students": "15,000+ Students",
        "placement": "IT & Core Recruiters",
    },
    {
        "id": "bits_hyd",
        "name": "BITS Pilani \u2014 Hyderabad Campus",
        "short": "BITS Hyd",
        "icon": "\U0001f3db\ufe0f",
        "type": "Private Deemed University",
        "location": "Shameerpet, Hyderabad",
        "color": "#58a6ff",
        "desc": "200-acre residential campus, 15,000 sq ft commercial complex, 24/7 medical center (Medicity tie-up).",
        "tags": ["Residential", "Campus Shops", "Medical", "SBI ATM", "Post Office"],
        "ranking": "NIRF Eng #25",
        "students": "3,500+ Students",
        "placement": "\u20b960.75L Highest / \u20b930L Avg CSE",
    },
    {
        "id": "isb_hyd",
        "name": "Indian School of Business (ISB) Hyderabad",
        "short": "ISB Hyd",
        "icon": "\U0001f4bc",
        "type": "Private Business School",
        "location": "Gachibowli, Hyderabad",
        "color": "#7c5cbf",
        "desc": "AACSB & SAQS accredited flagship 1-year PGP equivalent to a global MBA, domestic average package of \u20b933.25 LPA, highest \u20b91.56 Crore.",
        "tags": ["MBA", "PGP", "AACSB", "Placements", "Consulting"],
        "ranking": "FT Global MBA #31",
        "students": "900+ Students",
        "placement": "\u20b91.56 Crore Highest Package",
    },
    {
        "id": "imt_hyd",
        "name": "IMT Hyderabad",
        "short": "IMT Hyd",
        "icon": "\U0001f4c8",
        "type": "Private Business School",
        "location": "Shamshabad, Hyderabad",
        "color": "#f0883e",
        "desc": "30-acre green campus, 2-year PGDM programs, 14-week corporate internships, scholarships including 95% waiver for EWS and female diversity refunds.",
        "tags": ["PGDM", "Internships", "Scholarships", "Residential", "AICTE"],
        "ranking": "NIRF Mgmt #84",
        "students": "480+ Students",
        "placement": "\u20b925.0L Highest Package",
    },
    {
        "id": "ibs_hyd",
        "name": "ICFAI Business School (IBS) Hyderabad",
        "short": "IBS Hyd",
        "icon": "\U0001f4ca",
        "type": "Private Business School",
        "location": "Donthanapally, Hyderabad",
        "color": "#39c5b9",
        "desc": "91-acre campus, AACSB & NAAC A++ accredited MBA, case-study pedagogy with 6,000+ case studies, placement average of \u20b99.82 LPA.",
        "tags": ["MBA", "Case Study", "AACSB", "Placements", "NAAC A++"],
        "ranking": "NIRF Mgmt #40",
        "students": "2,400+ Students",
        "placement": "\u20b921.0L Highest / \u20b99.82L Avg",
    },
    {
        "id": "omc",
        "name": "Osmania Medical College (OMC)",
        "short": "OMC",
        "icon": "\U0001fa7a",
        "type": "Government Medical College",
        "location": "Koti, Hyderabad",
        "color": "#3fb950",
        "desc": "Established in 1846, central node for 10 specialized teaching hospitals (6,000+ beds), \u20b910,000/yr tuition, 1-year service bond with \u20b920L penalty.",
        "tags": ["NEET", "MBBS", "MD/MS", "Service Bond", "Clinical Exposure"],
        "ranking": "NIRF Medical #25",
        "students": "1,250+ Students",
        "placement": "Clinicals in 10 teaching hospitals",
    },
    {
        "id": "nizam",
        "name": "Nizam College Hyderabad",
        "short": "Nizam",
        "icon": "\U0001f3db\ufe0f",
        "type": "Constituent College of Osmania University",
        "location": "Basheerbagh, Hyderabad",
        "color": "#d29922",
        "desc": "Established in 1887, 20-acre historical campus, regular and self-financed UG/PG programs (e.g. B.Sc Data Science), TASK-registered placements.",
        "tags": ["DOST", "B.Sc Data Science", "Autonomous", "TASK Placements", "Hostel"],
        "ranking": "Arts Band 51-100",
        "students": "2,200+ Students",
        "placement": "TASK Placements cell",
    },
    {
        "id": "st_francis",
        "name": "St. Francis College for Women",
        "short": "St. Francis",
        "icon": "\U0001f469\u200d\U0001f393",
        "type": "Autonomous Minority College",
        "location": "Begumpet, Hyderabad",
        "color": "#4f8ef7",
        "desc": "Established in 1959, NAAC A++ grade, online admissions with minority policies, median UG package of \u20b94.0 LPA and PG package of \u20b97.60 LPA.",
        "tags": ["NAAC A++", "Women", "Admissions", "Placements", "Minority Quota"],
        "ranking": "NAAC A++ Grade",
        "students": "3,000+ Students",
        "placement": "\u20b97.60L PG Avg Package",
    },
    {
        "id": "jntuh",
        "name": "JNTU Hyderabad (JNTUH)",
        "short": "JNTUH",
        "icon": "\u2699\ufe0f",
        "type": "State University",
        "location": "Kukatpally, Hyderabad",
        "color": "#e3b341",
        "desc": "State-level engineering pathway via TS EAMCET, offers B.Tech/M.Tech programs, average placement package of \u20b96.00 LPA.",
        "tags": ["TS EAMCET", "State University", "B.Tech", "Placements"],
        "ranking": "NIRF Eng #83",
        "students": "8,000+ Students",
        "placement": "\u20b96.00L Avg Package",
    },
    {
        "id": "cbit",
        "name": "Chaitanya Bharathi Institute of Technology (CBIT)",
        "short": "CBIT",
        "icon": "\U0001f3eb",
        "type": "Autonomous Private Institute",
        "location": "Gandipet, Hyderabad",
        "color": "#4f8ef7",
        "desc": "Top autonomous engineering college, TS EAMCET/JEE admissions, B.Tech intake of 1,700+ students, highest CTC of \u20b954.00 LPA, average CSE \u20b96.50 LPA.",
        "tags": ["TS EAMCET", "Gandipet", "Autonomous", "Placements", "Engineering"],
        "ranking": "NIRF Eng #151",
        "students": "5,400+ Students",
        "placement": "\u20b954.0L Highest / \u20b96.50L Avg",
    },
    {
        "id": "griet",
        "name": "Gokaraju Rangaraju Institute (GRIET)",
        "short": "GRIET",
        "icon": "\U0001f4d0",
        "type": "Autonomous Private Institute",
        "location": "Bachupally, Hyderabad",
        "color": "#f0883e",
        "desc": "Autonomous engineering college, TS EAMCET admissions, B.Tech average package of \u20b99.27 LPA, highest package of \u20b951.60 LPA.",
        "tags": ["TS EAMCET", "Bachupally", "Placements", "Autonomous"],
        "ranking": "NIRF Eng #165",
        "students": "4,500+ Students",
        "placement": "\u20b951.60L Highest / \u20b99.27L Avg",
    },
    {
        "id": "vnr_vjiet",
        "name": "VNR VJIET",
        "short": "VNR VJIET",
        "icon": "\U0001f9ea",
        "type": "Autonomous Private Institute",
        "location": "Bachupally, Hyderabad",
        "color": "#39c5b9",
        "desc": "Autonomous engineering college, admissions via TS EAMCET, high-capacity B.Tech intake of 1,900+ students, average package of \u20b96.00 LPA.",
        "tags": ["TS EAMCET", "Bachupally", "High Intake", "Placements"],
        "ranking": "NIRF Eng #101",
        "students": "6,000+ Students",
        "placement": "\u20b948.00L Highest / \u20b96.00L Avg",
    },
    {
        "id": "vardhaman",
        "name": "Vardhaman College of Engineering",
        "short": "Vardhaman",
        "icon": "\U0001f52c",
        "type": "Autonomous Private Institute",
        "location": "Shamshabad, Hyderabad",
        "color": "#3fb950",
        "desc": "Autonomous engineering college, TS EAMCET admissions, median placement package of \u20b96.25 LPA, average package of \u20b95.74 LPA for CSE.",
        "tags": ["TS EAMCET", "Shamshabad", "Autonomous", "Placements"],
        "ranking": "NIRF Eng #143",
        "students": "3,800+ Students",
        "placement": "\u20b96.25L Median Package",
    },
    {
        "id": "anurag",
        "name": "Anurag University",
        "short": "Anurag",
        "icon": "\U0001f6f0\ufe0f",
        "type": "Private University",
        "location": "Venkatapur, Hyderabad",
        "color": "#7c5cbf",
        "desc": "Private university, admissions via TS EAMCET and JEE Main, offers B.Tech programs, average placement package of \u20b95.20 LPA.",
        "tags": ["TS EAMCET", "JEE Main", "Private University", "Placements"],
        "ranking": "NIRF Eng #150",
        "students": "5,000+ Students",
        "placement": "\u20b95.20L Avg Package",
    },
    {
        "id": "iare",
        "name": "Institute of Aeronautical Engineering (IARE)",
        "short": "IARE",
        "icon": "\u2708\ufe0f",
        "type": "Autonomous Private Institute",
        "location": "Dundigal, Hyderabad",
        "color": "#58a6ff",
        "desc": "Autonomous engineering college, admissions via TS EAMCET, average package of \u20b97.00 LPA for CSE, highest package of \u20b960.00 LPA.",
        "tags": ["TS EAMCET", "Dundigal", "Aeronautical", "Placements"],
        "ranking": "NIRF Eng #151-200",
        "students": "3,000+ Students",
        "placement": "\u20b97.00L Avg Package",
    },
]

COLLEGE_MAP = {c["id"]: c for c in COLLEGES}

# Colleges whose data is actually indexed in the vector store / structured tools.
INDEXED_COLLEGE_IDS = {
    "general", "iith", "iiith", "nalsar", "nims", "hcu",
    "osmania", "bits_hyd", "omc",
}

# ── LLM Settings ──────────────────────────────────────────────────────────────
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))
