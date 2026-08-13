"""
chat.py — Chat page with message history, suggestions, and voice input.
Extracted from app.py lines 1549-2063.
"""

import os
import html
import textwrap
import streamlit as st
from datetime import datetime
from typing import Optional

from core.config import COLLEGE_MAP, is_any_api_configured
from core.data_loader import load_contacts, load_events
from ui.components import get_college_icon_html, get_college_logo_html, safe_hex_to_rgb, render_message


# ── College-specific quick suggestions ────────────────────────────────────────

_COLLEGE_SUGGESTIONS = {
    "general":  ["\U0001f4bc Compare placements", "\U0001f393 Scholarship details", "\U0001f3e0 Hostel facilities", "\U0001f4cb Admission cutoffs", "\U0001f4da Library timings", "\U0001f4dd Bonafide certificate", "\U0001f393 CGPA calculation", "\U0001f52c Technical clubs"],
    "iith":     ["\U0001f4bc Compare placements", "\U0001f393 Scholarship details", "\U0001f3e0 Hostel facilities", "\U0001f4cb Admission cutoffs", "\U0001f4d0 Fractal Academics model", "\U0001f4b0 IITH fee structure", "\U0001f68c Bus timing from Nagole", "\U0001f393 MCM scholarship"],
    "iiith":    ["\U0001f4bc Compare placements", "\U0001f393 Scholarship details", "\U0001f3e0 Hostel facilities", "\U0001f4cb Admission cutoffs", "\U0001f4bb Ada cluster specs", "\U0001f37d\ufe0f Kadamba dining menu", "\U0001f3e0 Hostel allocation policy", "\U0001f4dd UGEE exam details"],
    "nalsar":   ["\U0001f4bc Compare placements", "\U0001f393 Scholarship details", "\U0001f3e0 Hostel facilities", "\U0001f4cb Admission cutoffs", "\U0001f4cb CLAT cutoff rank", "\U0001f4b0 NALSAR fee structure", "\u2696\ufe0f LLB programs offered", "\U0001f3db\ufe0f Law school facilities"],
    "nims":     ["\U0001f4bc Compare placements", "\U0001f393 Scholarship details", "\U0001f3e0 Hostel facilities", "\U0001f4cb Admission cutoffs", "\U0001fa7a NEET PG cutoff by category", "\U0001f4cb MD/MS admission", "\U0001f4b0 DNB program fee", "\U0001f3e5 BPT eligibility"],
    "hcu":      ["\U0001f4bc Compare placements", "\U0001f393 Scholarship details", "\U0001f3e0 Hostel facilities", "\U0001f4cb Admission cutoffs", "\U0001f3e0 50 km hostel rule", "\U0001f4f1 Samarth portal process", "\U0001f4b0 Hostel fee SC/ST", "\U0001f4dd GRE requirements"],
    "osmania":  ["\U0001f4bc Compare placements", "\U0001f393 Scholarship details", "\U0001f3e0 Hostel facilities", "\U0001f4cb Admission cutoffs", "\U0001f4ca SGPA CGPA formula", "\U0001f4dd Internal exam format", "\u2705 Attendance requirement", "\U0001f4cb CBCS credit system"],
    "bits_hyd": ["\U0001f4bc Compare placements", "\U0001f393 Scholarship details", "\U0001f3e0 Hostel facilities", "\U0001f4cb Admission cutoffs", "\U0001f6d2 Campus shops list", "\U0001f3e5 Medical center timings", "\U0001f3e6 SBI branch on campus", "\U0001f48a Pharmacy details"],
}

# Quick action bar definitions
_QUICK_ACTIONS = [
    ("\U0001f4bc Placements", "What are the latest placement records, highest package, average package and top recruiters?"),
    ("\U0001f3e0 Hostel", "Tell me about the hostel rooms, facilities, mess fees and hostel rules."),
    ("\U0001f393 Scholarships", "What scholarships, fee waivers and financial aid options are available?"),
    ("\U0001f4cb Cutoffs", "What are the cutoff ranks and admission eligibility criteria?"),
    ("\U0001f4de Faculty", "Show me the faculty directory, department HODs and office contact details."),
]


def _send_message(user_input: str):
    """Process a user message through the chatbot and update session state."""
    if not user_input.strip():
        return

    if not is_any_api_configured():
        st.error("\u26a0\ufe0f **API Key not configured!** Please add your `GOOGLE_API_KEY` (Gemini) or `OPENAI_API_KEY` (OpenAI) to the `.env` file and restart.")
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

    # Typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown(f"""
        <div class="message bot">
            <div class="message-avatar">{get_college_icon_html("\U0001f393")}</div>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    response = ""
    tool_used = ""
    resp_time_ms = 0
    query_id = None

    try:
        chatbot = _get_chatbot()

        for event in chatbot.stream_chat(contextual_input, session_id=st.session_state.session_id):
            if event["type"] == "tool":
                tool_used = event["name"]
            elif event["type"] == "content":
                response += event["text"]
                typing_placeholder.markdown(f"""
                <div class="message bot">
                    <div class="message-avatar">{get_college_icon_html("\U0001f393")}</div>
                    <div style="width:100%">
                        <div class="message-bubble">{response}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            elif event["type"] == "error":
                response = event["text"]
                tool_used = "error"
            elif event["type"] == "time":
                resp_time_ms = event["ms"]
                response = event["full_text"]

        # Log to database
        if response and not response.startswith("\U0001f527") and tool_used != "error":
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
                    response_time_ms=resp_time_ms,
                )
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"DB logging error: {e}")

    except Exception as e:
        import traceback
        import logging
        logging.getLogger(__name__).error(f"Chatbot error: {e}\n{traceback.format_exc()}")
        response = (
            "\U0001f527 **System Error**: I'm having trouble connecting right now.\n\n"
            f"**Error Details**: `{str(e)}`\n\n"
            "Please check:\n"
            "1. Your `GOOGLE_API_KEY` or `OPENAI_API_KEY` is valid in `.env`\n"
            "2. Vector store is initialized (`python initialize.py`)\n"
            "3. All dependencies are installed (`pip install -r requirements.txt`)"
        )
        tool_used = "error"
        resp_time_ms = 0

    typing_placeholder.empty()

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime("%H:%M"),
        "tool_used": tool_used,
        "query_id": query_id,
        "response_time_ms": resp_time_ms,
    })


def _get_chatbot():
    """Lazy-load chatbot."""
    from core.agent import CampusChatbot
    return CampusChatbot()


def _give_feedback(query_id: Optional[int], rating: int, msg_idx: int):
    """Record user feedback in the database."""
    try:
        from core.database import log_feedback
        if query_id:
            log_feedback(query_id, rating)
        st.session_state.feedback_given.add(msg_idx)
        st.success("\u2705 Thanks for your feedback!" if rating == 1 else "\U0001f4dd Feedback recorded. We'll improve!")
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Feedback error: {e}")


def _build_mic_html(r: int, g: int, b: int, college_color: str) -> str:
    """Build the voice mic button HTML with speech recognition JS."""
    return f"""
    <button id="voicemicbtn" type="button" style="
        width: 100%; height: 42px;
        background: rgba({r}, {g}, {b}, 0.08);
        border: 1px solid rgba({r}, {g}, {b}, 0.25);
        border-radius: 8px; color: {college_color}; font-size: 1.25rem;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        transition: all 0.2s ease; position: relative; overflow: hidden;
    " title="Speak your question">
        <span id="micicon">\U0001f3a4</span>
        <div id="micwavecontainer" style="display: none; align-items: center; justify-content: center; gap: 3px; height: 16px;">
            <div style="width: 3px; height: 100%; background-color: #EF4444; border-radius: 1px; animation: micbounce 0.8s ease-in-out infinite alternate;"></div>
            <div style="width: 3px; height: 100%; background-color: #EF4444; border-radius: 1px; animation: micbounce 0.5s ease-in-out infinite alternate; animation-delay: 0.15s;"></div>
            <div style="width: 3px; height: 100%; background-color: #EF4444; border-radius: 1px; animation: micbounce 0.7s ease-in-out infinite alternate; animation-delay: 0.3s;"></div>
            <div style="width: 3px; height: 100%; background-color: #EF4444; border-radius: 1px; animation: micbounce 0.6s ease-in-out infinite alternate; animation-delay: 0.05s;"></div>
        </div>
    </button>
    <script>
    (function() {{
        const btn = document.getElementById("voicemicbtn");
        const icon = document.getElementById("micicon");
        const wave = document.getElementById("micwavecontainer");
        if (!btn) return;
        let recognition = null;
        let islistening = false;
        btn.addEventListener("click", () => {{
            if (islistening) {{ if (recognition) {{ recognition.stop(); }} return; }}
            let SpeechRecognition = null;
            let doc = document;
            try {{
                const parentWin = window.parent;
                if (parentWin && parentWin.document) {{
                    doc = parentWin.document;
                    SpeechRecognition = parentWin.SpeechRecognition || parentWin.webkitSpeechRecognition;
                }}
            }} catch (e) {{ console.warn("CORS restriction:", e); }}
            if (!SpeechRecognition) {{ SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition; }}
            if (!SpeechRecognition) {{ alert("Web Speech API is not supported in this browser. Please use Google Chrome, Microsoft Edge, or Apple Safari."); return; }}
            try {{
                recognition = new SpeechRecognition();
                recognition.lang = "en-IN";
                recognition.interimResults = true;
                recognition.continuous = false;
                islistening = true;
                btn.classList.add("listeningactive");
                icon.style.display = "none";
                wave.style.display = "flex";
                const container = doc.getElementsByClassName("stTextInput").item(0) || document.getElementsByClassName("stTextInput").item(0);
                const input = container ? container.getElementsByTagName("input").item(0) : null;
                const updateValue = (val) => {{
                    if (!input) return;
                    let setter = null;
                    try {{
                        if (window.parent && window.parent.HTMLInputElement) {{
                            setter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, "value").set;
                        }}
                    }} catch (err) {{}}
                    if (!setter) {{
                        try {{ setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set; }} catch (err) {{}}
                    }}
                    if (setter) {{ setter.call(input, val); }} else {{ input.value = val; }}
                    input.dispatchEvent(new Event("input", {{ bubbles: true }}));
                }};
                recognition.onresult = (event) => {{
                    let text = "";
                    for (let i = 0; i < event.results.length; ++i) {{ text += event.results.item(i).item(0).transcript; }}
                    updateValue(text);
                }};
                recognition.onend = () => {{ resetState(); }};
                recognition.onerror = (event) => {{
                    console.error("Speech recognition error:", event.error);
                    let msg = "Speech recognition error: " + event.error;
                    if (event.error === "not-allowed") {{ msg = "\U0001f3a4 Microphone access is blocked! Please click the camera/microphone icon in your browser's address bar to allow permissions for this website."; }}
                    else if (event.error === "no-speech") {{ msg = "\U0001f3a4 No speech detected. Please speak clearly into your microphone."; }}
                    alert(msg);
                    resetState();
                }};
                recognition.start();
            }} catch (e) {{ console.error("Failed to start Speech Recognition:", e); resetState(); }}
        }});
        function resetState() {{
            islistening = false;
            btn.classList.remove("listeningactive");
            icon.style.display = "inline";
            wave.style.display = "none";
            recognition = null;
        }}
    }})();
    </script>
    """


def _build_location_html(active_c: dict, college_color: str, r: int, g: int, b: int) -> str:
    """Build the campus location & directions card HTML."""
    import urllib.parse
    loc_query = f"{active_c.get('name')}, {active_c.get('location')}" if active_c.get("location") != "Pan-India" else active_c.get("name")
    maps_url = f"https://www.google.com/maps/dir/?api=1&destination={urllib.parse.quote_plus(loc_query)}"

    return f"""<style>
.location-directions-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 0.5rem;
    margin-bottom: 2.5rem;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 1.5rem;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    text-decoration: none !important;
}}
.location-directions-card:hover {{
    transform: translateY(-3px);
    border-color: {college_color};
    box-shadow: 0 12px 30px rgba({r}, {g}, {b}, 0.12);
}}
@keyframes radar {{
    0% {{ transform: scale(0.2); opacity: 0.8; }}
    100% {{ transform: scale(1.8); opacity: 0; }}
}}
.radar-ring {{
    position: absolute;
    width: 45px;
    height: 45px;
    border: 1.5px solid {college_color};
    border-radius: 50%;
    animation: radar 2s infinite;
}}
</style>
<a href="{maps_url}" target="_blank" style="text-decoration: none; color: inherit;">
    <div class="location-directions-card">
        <div style="width: 70px; height: 70px; background: radial-gradient(circle, rgba({r}, {g}, {b}, 0.15) 0%, rgba({r}, {g}, {b}, 0) 70%), linear-gradient(45deg, var(--border) 25%, transparent 25%), linear-gradient(-45deg, var(--border) 25%, transparent 25%), linear-gradient(45deg, transparent 75%, var(--border) 75%), linear-gradient(-45deg, transparent 75%, var(--border) 75%); background-size: 10px 10px; background-position: 0 0, 5px 0, 5px -5px, 0px 5px; border: 1px solid var(--border); border-radius: 12px; display: flex; align-items: center; justify-content: center; position: relative; flex-shrink: 0; overflow: hidden;">
            <div style="width: 14px; height: 14px; background: {college_color}; border: 2.5px solid var(--bg-surface); border-radius: 50%; box-shadow: 0 0 10px {college_color}; position: relative; z-index: 2;"></div>
            <div class="radar-ring"></div>
        </div>
        <div style="flex-grow: 1;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; color: {college_color}; margin-bottom: 0.25rem;">\U0001f4cd Location & Route Finder</div>
            <div style="font-family: 'Calistoga', Georgia, serif; font-size: 1.25rem; color: var(--text-primary); margin-bottom: 0.25rem; line-height: 1.2;">{active_c.get('name')}</div>
            <div style="font-size: 0.88rem; color: var(--text-secondary); font-family: 'Inter', sans-serif;">Campus Address: {active_c.get('location')}</div>
        </div>
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1rem; background: {college_color}; border-radius: 8px; color: #ffffff; font-weight: 600; font-size: 0.82rem; font-family: 'Inter', sans-serif; box-shadow: 0 4px 12px rgba({r}, {g}, {b}, 0.3); flex-shrink: 0;">
            \U0001f9ed Directions
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </div>
    </div>
</a>"""


def render():
    """Render the Chat page."""
    active_c = COLLEGE_MAP.get(st.session_state.get("selected_college") or "", {})

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
""")
        c_names = [c["name"] for c in COLLEGE_MAP.values()]
        selected_name = st.selectbox("Quick Select Institution Node", ["-- Select Institution --"] + c_names)
        if selected_name != "-- Select Institution --":
            selected_c = next(c for c in COLLEGE_MAP.values() if c["name"] == selected_name)
            st.session_state.selected_college = selected_c["id"]
            st.session_state.messages = []
            st.rerun()

        st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
        if st.button("Browse All Colleges in Overview \U0001f3db", use_container_width=True):
            st.session_state.page = "\U0001f3e0 Overview"
            st.rerun()
        return

    college_color = active_c.get("color", "#0052FF")
    r_c, g_c, b_c = safe_hex_to_rgb(college_color)

    # Active college header
    st.markdown(f"""
<div style="background-color:#0F172A;background-image:radial-gradient(rgba(255,255,255,0.04) 1px,transparent 1px);background-size:24px 24px;border:1px solid #1E293B;border-radius:16px;padding:2.25rem;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin-bottom:1.5rem;">
    <div style="display:inline-flex;align-items:center;gap:0.6rem;border:1px solid rgba(0,82,255,0.35);background:rgba(0,82,255,0.08);border-radius:9999px;padding:0.3rem 1rem;margin-bottom:1rem;">
        <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#0052FF;box-shadow:0 0 6px #0052FF;"></span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.15em;color:#60a5fa;">Active Node</span>
    </div>
    <div style="font-size:1.85rem;font-weight:400;font-family:'Calistoga',Georgia,serif;color:#FFFFFF;margin:0 0 0.5rem 0;letter-spacing:-0.01em;">{active_c.get('name','CampusAI')}</div>
    <div style="color:#94A3B8;margin:0 0 1.1rem 0;font-family:'Inter',sans-serif;font-size:0.92rem;">Query statistics, admissions, placement logs, and calendar schedules directly from the app's local database.</div>
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
        <span style="display:inline-flex;align-items:center;padding:0.2rem 0.55rem;background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.3);border-radius:4px;font-size:0.68rem;font-weight:500;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">\U0001f916 GPT-4o mini</span>
        <span style="display:inline-flex;align-items:center;padding:0.2rem 0.55rem;background:rgba(0,82,255,0.15);color:#60a5fa;border:1px solid rgba(0,82,255,0.3);border-radius:4px;font-size:0.68rem;font-weight:500;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">\U0001f4da KNOWLEDGE CHUNKS</span>
        <span style="display:inline-flex;align-items:center;padding:0.2rem 0.55rem;background:#10b981;color:#ffffff;border:1px solid #10b981;border-radius:4px;font-size:0.68rem;font-weight:500;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">\u26a1 REAL-TIME RAG</span>
    </div>
</div>
""", unsafe_allow_html=True)

    # College info bar with tags and maps link
    active_college_id = st.session_state.get("selected_college")
    if active_college_id and active_college_id != "general":
        import urllib.parse
        loc_query = f"{active_c.get('name')}, {active_c.get('location')}" if active_c.get("location") != "Pan-India" else active_c.get("name")
        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={urllib.parse.quote_plus(loc_query)}"
        tags_html = " ".join([f'<span class="college-tag">{t}</span>' for t in active_c.get("tags", [])])

        st.markdown(f"""
        <div class="active-college-info" style="background:var(--bg-surface);border:1px solid var(--border);padding:1.25rem;border-radius:8px;margin-bottom:1.5rem;font-size:0.88rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;flex-wrap:wrap;gap:0.5rem;">
                <span style="font-weight:600;color:var(--text-primary);">\U0001f4cd Location: <span style="font-weight:normal;color:var(--text-secondary);">{active_c.get('location')}</span></span>
                <span style="font-weight:600;color:var(--text-primary);">\U0001f3db\ufe0f Type: <span style="font-weight:normal;color:var(--text-secondary);">{active_c.get('type')}</span></span>
            </div>
            <div style="color:var(--text-secondary);line-height:1.5;margin-bottom:0.75rem;">{active_c.get('desc')}</div>
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;margin-top:0.75rem;">
                <div style="display:flex;gap:0.35rem;flex-wrap:wrap;">{tags_html}</div>
                <a href="{maps_url}" target="_blank" style="text-decoration:none; display:inline-flex; align-items:center; gap:0.4rem; padding:0.35rem 0.75rem; background:rgba(0,82,255,0.08); border:1px solid rgba(0,82,255,0.25); border-radius:6px; color:#0052FF; font-weight:600; font-size:0.78rem; transition: background 0.2s;">
                    \U0001f5fa\ufe0f Get Directions on Maps
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Quick suggestion chips
    suggestions = _COLLEGE_SUGGESTIONS.get(st.session_state.selected_college, _COLLEGE_SUGGESTIONS["general"])

    st.markdown(f"""
    <style>
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: var(--bg-surface) !important;
        border: 2px solid {college_color} !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        box-shadow: 0 10px 30px rgba({r_c}, {g_c}, {b_c}, 0.1) !important;
        margin-top: 1.5rem !important;
        margin-bottom: 2.5rem !important;
    }}
    </style>
    """.replace("\n", " "), unsafe_allow_html=True)

    with st.container(border=True):
        if not st.session_state.messages:
            st.markdown(f"""
            <div style="font-size:0.75rem;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.05em;margin-top:0.5rem;margin-bottom:0.75rem;">
                \U0001f525 MOST ASKED ABOUT {active_c.get('short','').upper()}
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(4)
            for i, sug in enumerate(suggestions):
                parts = sug.split(" ", 1)
                query_text = parts[1].strip() if len(parts) > 1 else sug
                display_label = query_text.upper()
                if cols[i % 4].button(display_label, key=f"sug_{i}", use_container_width=True):
                    _send_message(query_text)
                    st.rerun()

            st.divider()

        if not st.session_state.messages:
            st.markdown(f"""
            <div class="empty-state">
                <span class="empty-state-icon">{active_c.get('icon','\U0001f44b')}</span>
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
                render_message(msg, idx, st.session_state.feedback_given)

                # Feedback buttons for bot messages
                if msg["role"] == "assistant" and idx not in st.session_state.feedback_given:
                    col1, col2, col3 = st.columns([1, 0.15, 0.15])
                    with col2:
                        if st.button("\U0001f44d", key=f"up_{idx}", help="Helpful"):
                            _give_feedback(msg.get("query_id"), 1, idx)
                    with col3:
                        if st.button("\U0001f44e", key=f"dn_{idx}", help="Not helpful"):
                            _give_feedback(msg.get("query_id"), -1, idx)

            if st.session_state.messages:
                st.markdown(
                    '<div id="chat-bottom"></div>'
                    '<script>document.getElementById("chat-bottom").scrollIntoView({behavior:"smooth"});</script>',
                    unsafe_allow_html=True,
                )

        # Quick Actions Row
        st.markdown(f"""
        <div style="font-size:0.65rem;font-weight:700;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.12em;margin-top:1.5rem;margin-bottom:0.6rem; font-family:'JetBrains Mono',monospace">
            \u26a1 Quick Actions
        </div>
        """, unsafe_allow_html=True)

        qa_cols = st.columns(5)
        for col_idx, (label, query_text) in enumerate(_QUICK_ACTIONS):
            if qa_cols[col_idx].button(label, key=f"qa_{col_idx}", use_container_width=True):
                _send_message(query_text)
                st.rerun()

        st.markdown("<div style='margin-bottom:0.75rem'></div>", unsafe_allow_html=True)

        # Input area
        with st.form(key="chat_form", clear_on_submit=True):
            col_input, col_mic, col_send = st.columns([5.2, 0.6, 1.2])
            with col_input:
                user_input = st.text_input(
                    "Message",
                    placeholder="Type your question here (e.g. library timings, placement statistics)...",
                    label_visibility="collapsed",
                    key="chat_input",
                )
            with col_mic:
                mic_html = _build_mic_html(r_c, g_c, b_c, college_color)
                st.markdown(textwrap.dedent(mic_html).strip().replace("\n", " "), unsafe_allow_html=True)
            with col_send:
                send_btn = st.form_submit_button("Send \U0001f680", use_container_width=True)

            if send_btn and user_input and user_input.strip():
                _send_message(user_input.strip())
                st.rerun()

        # Response stats
        if st.session_state.messages:
            bot_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]
            if bot_msgs:
                avg_time = sum(m.get("response_time_ms", 0) for m in bot_msgs) / len(bot_msgs)
                st.caption(f"\U0001f4ac {len(bot_msgs)} responses | \u26a1 Avg: {avg_time:.0f}ms")

    # Location & Directions Finder
    selected_c_id = st.session_state.get("selected_college")
    if selected_c_id and selected_c_id != "general":
        st.markdown('<h3 style="font-family:\'Calistoga\',serif;font-weight:400;margin-top:2.5rem;margin-bottom:1rem;color:var(--text-primary);">\U0001f4cd Campus Location & Directions</h3>', unsafe_allow_html=True)
        location_html = _build_location_html(active_c, college_color, r_c, g_c, b_c)
        st.markdown(textwrap.dedent(location_html).strip().replace("\n", " "), unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='font-family:\"Calistoga\",serif;font-weight:400;margin-top:2.5rem;margin-bottom:1rem;color:var(--text-primary);'>\U0001f4cd Campus Location & Directions</h3>", unsafe_allow_html=True)
        st.info("\U0001f3eb **No College Selected**: Please select a specific college from the **Overview** page to view campus location details and calculate maps directions.")
