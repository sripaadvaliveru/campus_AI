"""
theme.py — CSS injection for dark/light mode and static style overrides.
Extracted from the 300+ lines of inline CSS in app.py.
"""

import streamlit as st
from core.config import ROOT


def load_css(selected_college: str = None):
    """Load the base CSS file and inject theme + static overrides."""
    css_path = ROOT / "ui" / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Constrain width when a specific college is selected
    if selected_college:
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
          --bg-base:        #0F172A;
          --bg-surface:     #1E293B;
          --bg-card:        #1E293B;
          --text-primary:   #F8FAFC;
          --text-secondary: #94A3B8;
          --text-muted:     #475569;
          --border:         #334155;
          --accent:         #0052FF;
          --accent-gradient: linear-gradient(135deg, #0052FF, #4D7CFF);
          --accent-fore:    #ffffff;
          --accent-sec:     #3B82F6;
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
          --bg-base:        #FAFAFA;
          --bg-surface:     #ffffff;
          --bg-card:        #ffffff;
          --text-primary:   #0F172A;
          --text-secondary: #64748B;
          --text-muted:     #94A3B8;
          --border:         #E2E8F0;
          --accent:         #0052FF;
          --accent-gradient: linear-gradient(135deg, #0052FF, #4D7CFF);
          --accent-fore:    #ffffff;
          --accent-sec:     #3B82F6;
          --bg-sidebar:     #F8FAFC;
        }
        h1, h2, h3, h4, .calistoga-header {
          font-family: 'Calistoga', Georgia, serif !important;
          font-weight: 400 !important;
          letter-spacing: -0.01em !important;
        }
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
        .campus-header h1, .campus-header h2,
        .campus-header [style*="color:#FFFFFF"],
        .campus-header [style*="color: #FFFFFF"] {
          color: #FFFFFF !important;
        }
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

    [data-testid="stMarkdownContainer"] > p,
    [data-testid="stMarkdownContainer"] li {
      color: var(--text-secondary);
    }
    [data-testid="stMarkdownContainer"] [style*="color:"] {
      color: inherit;
    }

    hr { background-color: var(--border) !important; }

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

    @keyframes micbounce {
      0% { transform: scaleY(0.2); }
      100% { transform: scaleY(1.0); }
    }
    @keyframes micpulse {
      0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
      70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
      100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    .listeningactive {
      animation: micpulse 1.5s infinite !important;
      background: rgba(239, 68, 68, 0.15) !important;
      border-color: rgba(239, 68, 68, 0.5) !important;
      color: #EF4444 !important;
    }
    </style>
    """

    st.markdown(theme_css, unsafe_allow_html=True)
    st.markdown(static_overrides, unsafe_allow_html=True)
