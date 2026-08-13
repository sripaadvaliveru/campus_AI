"""
components.py — Reusable UI components: SVG icons, logos, message bubbles, badges.
Extracted from app.py to keep page modules clean.
"""

import html
import streamlit as st


# ── SVG Icon Map ──────────────────────────────────────────────────────────────

_SVG_PATHS = {
    "\U0001f52c": '<path d="M6 18h8M3 22h14M12 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM12 9v13M9 3h3"/>',
    "\U0001f4bb": '<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>',
    "\u2696\ufe0f": '<path d="M16 16c0 2-3 3-3 3s-3-1-3-3m0-12h6M12 3v16m-8-3c0 2 3 3 3 3s3-1 3-3m-3-1c-1.5 0-3 1-3 3m9-3c1.5 0 3 1 3 3"/>',
    "\U0001f3e5": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 8v8M8 12h8"/>',
    "\U0001f393": '<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/><path d="M22 10v6"/>',
    "\U0001f4dc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
    "\U0001f3db\ufe0f": '<path d="M4 22h16M10 14h4M4 18h16M12 2L2 7h20L12 2zM5 14v4M9 14v4M13 14v4M17 14v4"/>',
    "\U0001f4bc": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "\U0001f4c8": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "\U0001f4ca": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "\U0001fa7a": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "\U0001f469\u200d\U0001f393": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 10L17 7.5L12 10l5 2.5L22 10z"/>',
    "\u2699\ufe0f": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "\U0001f4d0": '<path d="M21.3 8.3L15.7 2.7a2 2 0 0 0-2.8 0L2.7 12.9a2 2 0 0 0 0 2.8l5.6 5.6a2 2 0 0 0 2.8 0L21.3 11.1a2 2 0 0 0 0-2.8zM8.3 18.5l-2.8-2.8"/>',
    "\U0001f6f0\ufe0f": '<path d="M12 2L2 22l10-6 10 6L12 2z"/>',
    "\u2708\ufe0f": '<path d="M21 16V8a2 2 0 0 0-2-2h-3L9 12H3a2 2 0 0 0 0 4h6l7 6h3a2 2 0 0 0 2-2v-2"/>',
    "\U0001f1ee\U0001f1f3": '<path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/>',
    "\U0001f3eb": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "\U0001f9ea": '<path d="M6 18h8M3 22h14M12 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM12 9v13M9 3h3"/>',
}


def get_college_icon_html(icon_emoji: str, size: int = 22, color: str = "var(--accent)") -> str:
    """Convert emoji to a high-fidelity outline SVG icon."""
    path = _SVG_PATHS.get(icon_emoji, '<circle cx="12" cy="12" r="10"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}" '
        f'fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:middle;filter:drop-shadow(0 0 4px {color}40);">{path}</svg>'
    ).strip()


# ── College Logo Emblems ──────────────────────────────────────────────────────

_LOGO_MAP = {
    "general":     ("GEN",    "rgba(0, 82, 255, 0.05)",   "var(--accent)"),
    "iith":        ("IITH",   "rgba(240, 136, 62, 0.05)",  "#f0883e"),
    "iiith":       ("IIITH",  "rgba(57, 197, 185, 0.05)",  "#39c5b9"),
    "nalsar":      ("LAW",    "rgba(124, 92, 191, 0.05)",  "#7c5cbf"),
    "nims":        ("NIMS",   "rgba(63, 185, 80, 0.05)",   "#3fb950"),
    "hcu":         ("HCU",    "rgba(210, 153, 34, 0.05)",  "#d29922"),
    "osmania":     ("OU",     "rgba(227, 179, 65, 0.05)",  "#e3b341"),
    "bits_hyd":    ("BITS",   "rgba(88, 166, 255, 0.05)",  "#58a6ff"),
    "isb_hyd":     ("ISB",    "rgba(124, 92, 191, 0.05)",  "#7c5cbf"),
    "imt_hyd":     ("IMT",    "rgba(240, 136, 62, 0.05)",  "#f0883e"),
    "ibs_hyd":     ("IBS",    "rgba(57, 197, 185, 0.05)",  "#39c5b9"),
    "omc":         ("OMC",    "rgba(63, 185, 80, 0.05)",   "#3fb950"),
    "nizam":       ("NIZAM",  "rgba(210, 153, 34, 0.05)",  "#d29922"),
    "st_francis":  ("SFC",    "rgba(79, 142, 247, 0.05)",  "#4f8ef7"),
    "jntuh":       ("JNTUH",  "rgba(227, 179, 65, 0.05)",  "#e3b341"),
    "cbit":        ("CBIT",   "rgba(79, 142, 247, 0.05)",  "#4f8ef7"),
    "griet":       ("GRIET",  "rgba(240, 136, 62, 0.05)",  "#f0883e"),
    "vnr_vjiet":   ("VNR",    "rgba(57, 197, 185, 0.05)",  "#39c5b9"),
    "vardhaman":   ("VCE",    "rgba(63, 185, 80, 0.05)",   "#3fb950"),
    "anurag":      ("AU",     "rgba(124, 92, 191, 0.05)",  "#7c5cbf"),
    "iare":        ("IARE",   "rgba(88, 166, 255, 0.05)",  "#58a6ff"),
}

# Custom vector crests for top universities
_CUSTOM_LOGOS = {
    "iiith": """
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#39c5b9;filter:drop-shadow(0 0 4px rgba(57,197,185,0.3))">
                <path d="M12 2L2 12l10 10 10-10L12 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 6l6 6-6 6-6-6 6-6z" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">IIIT</span>
        </div>""",
    "iith": """
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#f0883e;filter:drop-shadow(0 0 4px rgba(240,136,62,0.3))">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 2"/>
                <circle cx="12" cy="12" r="2" fill="currentColor"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">IIT-H</span>
        </div>""",
    "nalsar": """
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#7c5cbf;filter:drop-shadow(0 0 4px rgba(124,92,191,0.3))">
                <path d="M3 21h18M5 21V10M19 21V10M9 21V10M15 21V10M4 6h16M12 3L3 6h18l-9-3z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">NALSAR</span>
        </div>""",
    "hcu": """
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#d29922;filter:drop-shadow(0 0 4px rgba(210,153,34,0.3))">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 0 6.5 22H20M4 19.5V4.5A2.5 2.5 0 0 1 6.5 2V17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 6v6M9 9h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">HCU</span>
        </div>""",
    "bits_hyd": """
        <div style="display:flex;align-items:center;gap:0.5rem">
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:#58a6ff;filter:drop-shadow(0 0 4px rgba(88,166,255,0.3))">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>
            <span style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.85rem;color:var(--text-primary)">BITS</span>
        </div>""",
}


def get_college_logo_html(college_id: str, size: int = 32, border_radius: str = "6px") -> str:
    """Render a stylized monogram or emblem for an institution."""
    if college_id in _CUSTOM_LOGOS:
        return _CUSTOM_LOGOS[college_id].format(size=size).strip()

    label, bg, color = _LOGO_MAP.get(college_id, ("CAMPUS", "rgba(0, 82, 255, 0.05)", "var(--accent)"))
    return (
        f'<div class="college-logo-badge" style="width:{size}px;height:{size}px;'
        f'background:{bg};border:1px solid {color}33;color:{color};border-radius:{border_radius};">'
        f'{label}</div>'
    ).strip()


# ── Chat Message Rendering ────────────────────────────────────────────────────

def render_message(msg: dict, idx: int, feedback_given: set):
    """Render a single chat message bubble with HTML."""
    role = msg["role"]
    content = msg["content"]
    timestamp = msg.get("timestamp", "")
    tool = msg.get("tool_used", "")

    safe_content = html.escape(content)

    if role == "user":
        st.markdown(f"""
        <div class="message user">
            <div class="message-avatar">\U0001f464</div>
            <div>
                <div class="message-bubble">{safe_content}</div>
                <div class="message-meta" style="text-align:right">{timestamp}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        tool_badge = (
            f'<span class="event-badge badge-academic" style="margin-left:0.5rem">{html.escape(tool)}</span>'
            if tool else ""
        )
        st.markdown(f"""
        <div class="message bot">
            <div class="message-avatar">{get_college_icon_html("\U0001f393")}</div>
            <div style="width:100%">
                <div class="message-bubble">{safe_content}</div>
                <div class="message-meta">{timestamp} {tool_badge}</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ── Hex to RGB helper ─────────────────────────────────────────────────────────

def hex_to_rgb(hex_str: str) -> tuple:
    """Convert hex color string to (r, g, b) tuple."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def safe_hex_to_rgb(hex_str: str) -> tuple:
    """Convert hex to RGB, returning default (0, 82, 255) on failure."""
    try:
        return hex_to_rgb(hex_str)
    except Exception:
        return (0, 82, 255)
