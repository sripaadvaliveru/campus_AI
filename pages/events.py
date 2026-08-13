"""
events.py — Academic calendar and events page.
Extracted from app.py lines 2232-2357.
"""

import json
from datetime import datetime, date
from itertools import groupby

import streamlit as st
from core.config import COLLEGE_MAP, DATA_DIR
from core.data_loader import load_events


def _get_month(ev):
    d = ev.get("date", "")
    if len(d) >= 7:
        try:
            return datetime.strptime(d[:7], "%Y-%m").strftime("%B %Y")
        except Exception:
            pass
    return "TBA"


def render():
    """Render the Events page."""
    active_college_id = st.session_state.get("selected_college") or "general"
    active_c = COLLEGE_MAP.get(active_college_id, {})

    st.markdown(f"""
    <div class="campus-header" style="background-color: #0F172A !important; background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important; background-size: 24px 24px !important; color: #F8FAFC !important; border-color: #1E293B !important; padding: 2.25rem !important; border-radius: 16px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;">
        <div class="section-label-badge">
            <span class="section-label-dot"></span>
            <span class="section-label-text">{active_c.get('short','CampusAI')}</span>
        </div>
        <h1 style="font-size:2.0rem;font-weight:400;font-family:'Calistoga',serif !important;color:#FFFFFF !important;margin:0 0 0.75rem 0;letter-spacing:-0.01em;">Academic Calendar & Events</h1>
        <p style="color:#94A3B8 !important;margin:0;">Complete academic year schedule \u2014 exams, fests, sports, holidays, and important deadlines.</p>
    </div>
    """, unsafe_allow_html=True)

    all_events = load_events()

    # Filter controls
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All", "Exam", "Cultural", "Technical", "Sports", "Holiday", "Academic", "Placement", "Social", "Orientation"],
            index=0,
        )
    with col2:
        semester_filter = st.selectbox(
            "Filter by Semester",
            ["All Semesters", "Odd Semester", "Even Semester"],
            index=0,
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

    badge_map = {
        "exam": "badge-exam", "cultural": "badge-cultural", "sports": "badge-sports",
        "holiday": "badge-holiday", "academic": "badge-academic", "placement": "badge-placement",
        "technical": "badge-academic", "social": "badge-cultural", "orientation": "badge-academic",
    }

    if not filtered:
        st.info("No events found for the selected filters.")
    else:
        grouped = {}
        for ev in filtered:
            month = _get_month(ev)
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
                        \U0001f4c5 {ev.get('date','TBA')} &nbsp;|&nbsp; {(ev.get('semester') or '').split('(')[0].strip()}
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
                    <div style="font-weight:600;color:var(--accent)">\U0001f4cc {dl.get('deadline','')}</div>
                    <div style="font-size:0.85rem;color:var(--text-secondary);margin-top:0.3rem">{dl.get('description','')}</div>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading deadlines: {e}")
