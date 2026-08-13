"""
compare.py — Side-by-side college comparison with charts.
Extracted from app.py lines 1375-1544.
"""

import re
import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.config import COLLEGES, COLLEGE_MAP, DATA_DIR


def _load_detailed_data(college_id: str) -> dict:
    """Load detailed JSON data for a specific college."""
    try:
        hyd_dir = DATA_DIR / "hyderabad"
        file_map = {
            "iith":     ("iith.json", None),
            "iiith":    ("iiith.json", None),
            "nalsar":   ("other_institutions.json", "NALSAR_University_of_Law"),
            "nims":     ("other_institutions.json", "NIMS_Medical_Sciences"),
            "hcu":      ("other_institutions.json", "University_of_Hyderabad_HCU"),
            "osmania":  ("other_institutions.json", "Osmania_University_CBCS"),
            "bits_hyd": ("other_institutions.json", "BITS_Pilani_Hyderabad"),
        }
        if college_id not in file_map:
            return {}
        filename, inner_key = file_map[college_id]
        filepath = hyd_dir / filename
        if not filepath.exists():
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if inner_key:
            return data.get(inner_key, {})
        return data
    except Exception:
        return {}


def _get_fees_str(college_id: str, data: dict) -> str:
    fees_map = {
        "iith":     "Rs. 1,68,993 (1st Sem Gen/OBC Total)",
        "iiith":    "Rs. 2,50,000 (1st Sem Tuition)",
        "nalsar":   "Rs. 3,17,000 (1st Year Gen Total)",
        "nims":     "Rs. 37,050 to 1,07,000 / year (varies)",
        "hcu":      "Rs. 3,850 (Hostel Admission)",
        "bits_hyd": "Rs. 2.45 Lakhs / sem Tuition (approx)",
    }
    return fees_map.get(college_id, "Varies \u2014 See Handbook")


def _get_hostel_policy(college_id: str, data: dict) -> str:
    policy_map = {
        "iith":     "On-campus housing available (Rs. 18,000/sem + dining)",
        "iiith":    "Mandatory residency. Palash/OBH/Bakul/Parijaat blocks",
        "hcu":      "Strict 50km radius Twin-Cities exclusion rule",
        "bits_hyd": "Fully residential self-contained campus township",
    }
    return policy_map.get(college_id, "Accommodation options available")


def _extract_placement_packages(college_id: str, detailed_data: dict, college_info: dict) -> tuple:
    highest = None
    average = None
    if college_id == "iiith" and "placements" in detailed_data:
        p25 = detailed_data["placements"].get("2025", {})
        highest = p25.get("highest_salary_LPA")
        average = p25.get("average_salary_LPA")
    elif college_id == "iith" and "placements_2024" in detailed_data:
        p24 = detailed_data["placements_2024"]
        highest = p24.get("highest_domestic_package_LPA")
        average = 21.28
    if highest is None or average is None:
        placement_str = college_info.get("placement", "")
        highest_match = re.search(r'(?:\u20b9|Rs\.?\s*)(\d+(?:\.\d+)?)\s*(?:L|Cr|Crore)?\s*Highest', placement_str, re.IGNORECASE)
        if highest_match:
            val = float(highest_match.group(1))
            if "Cr" in placement_str or "Crore" in placement_str:
                val *= 100.0
            highest = val
        avg_match = re.search(r'(?:\u20b9|Rs\.?\s*)(\d+(?:\.\d+)?)\s*(?:L)?\s*Avg', placement_str, re.IGNORECASE)
        if avg_match:
            average = float(avg_match.group(1))
    return highest, average


def render():
    """Render the Compare page."""
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
        d1 = _load_detailed_data(c1["id"])
        d2 = _load_detailed_data(c2["id"])

        comp_data = {
            "Comparison Category": [
                "Short Name", "Type", "Location", "NIRF Ranking",
                "Student Count", "Tuition / Hostel Fees",
                "Hostel Policies & Curfews", "Placement Records",
            ],
            c1["name"]: [
                c1["short"], c1["type"], c1["location"],
                c1.get("ranking", "N/A"), c1.get("students", "N/A"),
                _get_fees_str(c1["id"], d1), _get_hostel_policy(c1["id"], d1),
                c1.get("placement", "N/A"),
            ],
            c2["name"]: [
                c2["short"], c2["type"], c2["location"],
                c2.get("ranking", "N/A"), c2.get("students", "N/A"),
                _get_fees_str(c2["id"], d2), _get_hostel_policy(c2["id"], d2),
                c2.get("placement", "N/A"),
            ],
        }
        df_comp = pd.DataFrame(comp_data)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)

        # Plotly placement comparison
        h1, a1 = _extract_placement_packages(c1["id"], d1, c1)
        h2, a2 = _extract_placement_packages(c2["id"], d2, c2)

        categories = []
        highest_packages = []
        avg_packages = []

        if h1 or a1:
            categories.append(c1["short"])
            highest_packages.append(h1 or 0)
            avg_packages.append(a1 or 0)
        if h2 or a2:
            categories.append(c2["short"])
            highest_packages.append(h2 or 0)
            avg_packages.append(a2 or 0)

        if len(categories) > 0:
            st.markdown("### \U0001f4ca Placement Package Comparison (LPA)")
            fig = go.Figure(data=[
                go.Bar(name="Highest Package", x=categories, y=highest_packages, marker_color="#0052FF"),
                go.Bar(name="Average Package", x=categories, y=avg_packages, marker_color="#39c5b9"),
            ])
            fig.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white" if st.session_state.get("dark_mode", True) else "black"),
                yaxis=dict(title="Package in LPA (Lakhs Per Annum)", gridcolor="rgba(128,128,128,0.2)"),
                xaxis=dict(gridcolor="rgba(128,128,128,0.2)"),
            )
            st.plotly_chart(fig, use_container_width=True)
