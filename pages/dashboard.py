"""
dashboard.py — Campus intelligence dashboard page.
Extracted from app.py lines 2073-2224.
"""

import streamlit as st
import pandas as pd
from core.config import COLLEGE_MAP
from ui.components import get_college_icon_html


def render():
    """Render the Dashboard page."""
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

    # Stats Row
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
        (m1, s_total, "Total Queries", "\U0001f4ac"),
        (m2, s_today, "Today's Queries", "\U0001f4c5"),
        (m3, f"{s_sat}%", "Satisfaction Rate", "\u2b50"),
        (m4, f"{int(s_rt)}ms", "Avg Response", "\u26a1"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div style="font-size:1.5rem">{icon}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">\U0001f4a1 Common Questions Students Ask</div>', unsafe_allow_html=True)

    col_dash1, col_dash2 = st.columns(2)
    with col_dash1:
        st.markdown(f"""
        <div class="contact-card" style="margin-bottom:1.5rem; border-left: 3px solid var(--accent);">
            <div style="font-weight:600;font-size:1.1rem;color:var(--text-primary);margin-bottom:0.75rem;">\U0001f3db\ufe0f Example Topics by College</div>
            <div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);">
                1. <strong>IIT Hyderabad</strong> \u2014 placement eligibility & packages.<br>
                2. <strong>BITS Hyderabad</strong> \u2014 hostel facilities queries.<br>
                3. <strong>NALSAR Law</strong> \u2014 CLAT cutoff searches ahead of counseling.
            </div>
        </div>
        <div class="contact-card" style="margin-bottom:1.5rem; border-left: 3px solid var(--accent);">
            <div style="font-weight:600;font-size:1.1rem;color:var(--text-primary);margin-bottom:0.75rem;">\U0001f48e Example: Popular Scholarships</div>
            <div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);">
                \u2022 <strong>MCM Scholarship</strong> (IIT Hyderabad) \u2014 Full tuition waivers.<br>
                \u2022 <strong>Ishan Uday Scheme</strong> (NALSAR) \u2014 UGC North-East scheme.<br>
                \u2022 <strong>EWS PGDM Concessions</strong> (IMT) \u2014 95% waiver.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_dash2:
        st.markdown("""
        <div class="contact-card" style="margin-bottom:1.5rem; border-left: 3px solid var(--accent-sec);">
            <div style="font-weight:600;font-size:1.1rem;color:var(--text-primary);margin-bottom:0.75rem;">\U0001f4ca Illustrative Topic Mix (Not Live Analytics)</div>
            <div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);">
                \U0001f4c8 <strong>Placement Packages</strong> \u2014 commonly asked.<br>
                \U0001f4cb <strong>Admissions & Eligibility</strong> \u2014 frequently asked.<br>
                \U0001f3e0 <strong>Hostels & Mess rules</strong> \u2014 actively asked.<br>
                \U0001f91d <strong>Student Clubs & NSS</strong> \u2014 occasionally asked.
            </div>
        </div>
        <div class="contact-card" style="margin-bottom:1.5rem; border-left: 3px solid var(--accent-sec);">
            <div style="font-weight:600;font-size:1.1rem;color:var(--text-primary);margin-bottom:0.75rem;">\U0001f3af Sample Questions You Can Ask</div>
            <div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);">
                \u2022 "What is the highest package at IIIT-H?"<br>
                \u2022 "How is attendance calculated in Osmania?"<br>
                \u2022 "Is there a service bond penalty in OMC?"
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">CAMPUS INFORMATION CATEGORIES</div>', unsafe_allow_html=True)

    categories = [
        ("\U0001f393", "Academics", "CGPA, exams, attendance, grading, backlogs, CBCS system"),
        ("\U0001f3e0", "Hostel & Accommodation", "Hostel rules, facilities, mess timings, warden contact"),
        ("\U0001f4da", "Library Services", "Book lending, N-LIST access, digital resources, timings"),
        ("\U0001f4bc", "Placement & Careers", "Campus drives, internships, resume tips, salary packages"),
        ("\U0001f3ad", "Clubs & Activities", "Technical, cultural, sports, NSS, NCC, student council"),
        ("\U0001f3e5", "Health & Medical", "Health center, mental health, emergency contacts"),
        ("\U0001f4cb", "Documents & Certificates", "Bonafide, TC, migration, transcript, no dues"),
        ("\U0001f4b0", "Scholarships & Fees", "NSP, central/state schemes, fee payment, concessions"),
        ("\U0001f68c", "Transport & Facilities", "Bus routes, WiFi, canteen, sports, bank/ATM on campus"),
        ("\U0001f52c", "Research & Innovation", "R&D cell, patents, paper publication, conferences"),
        ("\U0001f3eb", "College Types", "Engineering, Medical, Arts, Management, Law, Architecture"),
        ("\U0001f310", "Higher Education", "GATE, GRE, CAT, IELTS, study abroad guidance"),
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

    # College Types Reference
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
    st.dataframe(df, use_container_width=True, hide_index=True)

    # FAQs
    st.divider()
    st.markdown('<div class="section-title">FREQUENTLY ASKED QUESTIONS</div>', unsafe_allow_html=True)

    faqs = [
        ("What is minimum attendance required?", "\U0001f4dd Most colleges require **75% minimum attendance**. Some (IITs, medical colleges) require **85%**. Students below 65% may be detained."),
        ("How is CGPA calculated?", "\U0001f4ca CGPA = Sum(Grade Points \u00d7 Credits) / Total Credits. Most universities use a 10-point scale where O=10, A+=9, A=8, B+=7, B=6, C=5, P=4."),
        ("How do I get a bonafide certificate?", "\U0001f4cb Apply at the college office with your ID card and a small fee (Rs. 20-50). Issued within 2-3 working days. Required for bank loans, internships, railway concession."),
        ("What is NSS and how to join?", "\U0001f91d NSS (National Service Scheme) is a Central Govt. program for 240 hours of community service. Register at the beginning of the academic year through your college's NSS unit."),
    ]

    for q, a in faqs:
        with st.expander(f"\U0001f4ac {q}"):
            st.markdown(a)
