"""
overview.py — College selection grid and landing page.
Extracted from app.py lines 1203-1370.
"""

import streamlit as st
import pandas as pd
from core.config import COLLEGES, COLLEGE_MAP, INDEXED_COLLEGE_IDS
from ui.components import get_college_icon_html, get_college_logo_html


def render():
    """Render the Overview page."""
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
        ">CampusAI \u2014 Campus Knowledge Assistant</span>
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
        ">curated campus data</span>.
    </div>
    <div style="color:#94A3B8;font-size:1.0rem;line-height:1.65;max-width:800px;font-family:'Inter',sans-serif;">
        CampusAI answers from curated campus reports, NIRF submittals, and handbooks with source citations,
        and is transparent about which institutions are actually indexed in its knowledge base.
    </div>
</div>
""", unsafe_allow_html=True)

    # Hero CTA buttons
    cta1, cta2, _pad = st.columns([1.3, 1.6, 3])
    with cta1:
        if st.button("Start Chat \u2192", use_container_width=True, key="hero_chat"):
            st.session_state.page = "\U0001f4ac Chat"
            st.rerun()
    with cta2:
        if st.button("Compare Colleges", use_container_width=True, key="hero_compare"):
            st.session_state.page = "\u2696\ufe0f Compare"
            st.rerun()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        st.markdown("""
        <div style="background:var(--bg-surface);border:1px solid var(--border);padding:1.5rem;border-radius:12px;height:100%;">
            <div style="font-weight:600;font-size:1rem;color:var(--accent);margin-bottom:0.5rem;">\U0001f3af AI Capability Showcase & Suggested Queries</div>
            <div style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;">
                \u2022 Compare placement packages (e.g. <i>"Compare highest CTC between IIT-H and IIIT-H"</i>)<br>
                \u2022 Get fee breakdown (e.g. <i>"What are the hostel and tuition fees at NALSAR?"</i>)<br>
                \u2022 Research scholarships (e.g. <i>"Which scholarships are available at HCU?"</i>)<br>
                \u2022 Find eligibility cutoffs (e.g. <i>"CLAT cutoff rank for NALSAR"</i>)
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_cap2:
        st.markdown("""
        <div style="background:var(--bg-surface);border:1px solid var(--border);padding:1.5rem;border-radius:12px;height:100%;">
            <div style="font-weight:600;font-size:1rem;color:var(--accent);margin-bottom:0.5rem;">\U0001f512 Why Trust CampusAI?</div>
            <p style="margin:0;font-size:0.85rem;color:var(--text-secondary);line-height:1.5;">
                Answers are retrieved from the <strong>indexed corpus</strong> \u2014 university handbooks, NIRF statistics, placement reports, fee structures, and brochures \u2014 with filename citations where available. Institutions without indexed data are labelled "General Knowledge" so you know when the model is not citing a source.
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
        if st.button("\u2696\ufe0f Compare Page", use_container_width=True):
            st.session_state.page = "\u2696\ufe0f Compare"
            st.rerun()

    st.markdown("""
    <div class="section-label-badge" style="margin-top: 1rem;">
        <span class="section-label-dot"></span>
        <span class="section-label-text">Directory</span>
    </div>
    <h2 style="font-family:'Calistoga',serif !important; font-weight:400; font-size:1.85rem; margin-top:0.25rem; margin-bottom:1.5rem; color:var(--text-primary);">Browse College Directory</h2>
    """, unsafe_allow_html=True)

    # College cards \u2014 3 columns
    for row_start in range(0, len(COLLEGES), 3):
        row_colleges = COLLEGES[row_start : row_start + 3]
        cols = st.columns(3)
        for i, c in enumerate(row_colleges):
            with cols[i]:
                is_verified = c["id"] in INDEXED_COLLEGE_IDS
                if is_verified:
                    verified_badge = '<span style="font-size:0.6rem;font-weight:600;color:#10b981;background:rgba(16,185,129,0.08);padding:0.15rem 0.45rem;border-radius:4px;border:1px solid rgba(16,185,129,0.15);">\u2713 VERIFIED SOURCE</span>'
                else:
                    verified_badge = '<span style="font-size:0.6rem;font-weight:600;color:#f59e0b;background:rgba(245,158,11,0.08);padding:0.15rem 0.45rem;border-radius:4px;border:1px solid rgba(245,158,11,0.2);">! GENERAL KNOWLEDGE \u2014 NOT IN KB</span>'
                logo_html = get_college_logo_html(c["id"], size=36)
                icon_html = get_college_icon_html(c["icon"], size=20)

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
                        <div style="font-weight: 600; color: var(--text-primary);">\U0001f3c6 {c.get('ranking', 'N/A')}</div>
                        <div style="font-weight: 500; color: var(--text-primary);">\U0001f4cd {c.get('location', 'N/A')}</div>
                        <div>\U0001f465 {c.get('students', 'N/A')}</div>
                        <div style="font-weight: 500; color: var(--accent);">\U0001f4bc {c.get('placement', 'N/A')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(
                    "View Details \u2192",
                    key=f"select_{c['id']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_college = c["id"]
                    st.session_state.messages = []
                    st.session_state.page = "\U0001f4ac Chat"
                    st.rerun()
