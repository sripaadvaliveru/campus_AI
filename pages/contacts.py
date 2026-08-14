"""
contacts.py — Faculty and staff directory page.
Extracted from app.py lines 2365-2453.
"""

import streamlit as st
import pandas as pd
from core.config import COLLEGE_MAP
from core.data_loader import load_contacts


def render():
    """Render the Contacts page."""
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
        return

    # Search and filter
    col1, col2 = st.columns([3, 2])
    with col1:
        search_term = st.text_input(
            "Search",
            placeholder="\U0001f50d  Search by name, department, designation, or specialization...",
            label_visibility="collapsed",
        )
    with col2:
        departments = sorted(set(c.get("department", "") for c in contacts))
        dept_filter = st.selectbox("Department", ["All Departments"] + departments, label_visibility="collapsed")

    filtered_contacts = contacts
    if search_term:
        st_lower = search_term.lower()
        filtered_contacts = [
            c for c in filtered_contacts
            if any(st_lower in str(c.get(f, "")).lower() for f in ["name", "designation", "department", "specialization"])
        ]
    if dept_filter != "All Departments":
        filtered_contacts = [c for c in filtered_contacts if c.get("department") == dept_filter]

    st.caption(f"Found {len(filtered_contacts)} contacts")
    st.divider()

    if not filtered_contacts:
        st.info("No contacts found. Try a different search term.")
    else:
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
                                    font-size:1.1rem;flex-shrink:0">\U0001f464</div>
                        <div>
                            <div class="contact-name">{contact.get('name','N/A')}</div>
                            <div class="contact-role">{contact.get('designation','')}</div>
                            <div class="contact-dept">{contact.get('department','')}</div>
                        </div>
                    </div>
                    <div style="height:1px;background:var(--border);margin:0.75rem 0"></div>
                    <div class="contact-info">
                        \U0001f4e7 <a href="mailto:{contact.get('email','')}" style="color:#4f8ef7;text-decoration:none">{contact.get('email','N/A')}</a><br>
                        \U0001f4de <a href="tel:{contact.get('phone','').replace('-','')}" style="color:#4f8ef7;text-decoration:none">{contact.get('phone','N/A')}</a><br>
                        \U0001f3e2 {contact.get('office_location','N/A')}<br>
                        \U0001f550 {contact.get('office_hours','N/A')}
                    </div>
                    {f'<div style="margin-top:0.5rem;font-size:0.75rem;color:var(--text-muted)">\U0001f52c {contact.get("specialization","")}</div>' if contact.get('specialization') else ''}
                </div>
                """, unsafe_allow_html=True)

    # Download contacts
    st.divider()
    df_contacts = pd.DataFrame(filtered_contacts)
    csv_data = df_contacts.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="\U0001f4e5 Download Contact List (CSV)",
        data=csv_data,
        file_name="campus_contacts.csv",
        mime="text/csv",
    )
