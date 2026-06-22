"""
Health Companion — Flat Minimalist UI Engine

Every element is rendered flat with clean borders, soft spacing, and restrained contrast.
Animations, 3D translations, and depth shadows are removed for a calmer aesthetic.
"""

from __future__ import annotations

import streamlit as st


def inject_theme() -> None:
    """Inject the complete premium CSS theme into the Streamlit app."""
    st.markdown(_GOOGLE_FONTS_LINK, unsafe_allow_html=True)
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


# ─── Google Fonts ─────────────────────────────────────────────────────────────

_GOOGLE_FONTS_LINK: str = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
      rel="stylesheet">
"""

# ─── Master CSS ───────────────────────────────────────────────────────────────

_CSS: str = """
/* ═══════════════════════════════════════════════════════════════════════
    HEALTH COMPANION — FLAT MINIMALIST THEME
   ═══════════════════════════════════════════════════════════════════════ */

:root {
  /* ── Color Palette ─────────────────────────────────────────────── */
    --bg-canvas: #F5F3EF;
    --surface: #FFFFFF;
    --text-primary: #17212E;
    --text-secondary: #4B5563;
    --text-muted: #6B7280;
    --accent: #23436A;
    --accent-light: #4E739B;
    --accent-dark: #172A45;
    --success: #496883;
  --warning: #EAB308;
  --danger: #DC2626;
  --info: #2563EB;

  /* ── Minimalist Shadow Matrix (Flat & Clean) ───────────────────── */
  --shadow-raised: none;
  --shadow-raised-hover: none;
  --shadow-pressed: none;
  --shadow-sunken: none;

  /* ── Glassmorphism Override (Flat) ─────────────────────────────── */
  --glass-bg: #FFFFFF;
    --glass-border: 1px solid rgba(19, 31, 45, 0.10);
  --glass-blur: none;

  /* ── Misc ──────────────────────────────────────────────────────── */
  --transition: none;
  --font: 'Inter', sans-serif;
}

/* ─── Global ────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    color: var(--text-primary);
    background-color: var(--bg-canvas) !important;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(35, 67, 106, 0.06), transparent 28%),
        linear-gradient(180deg, #FBFAF8 0%, var(--bg-canvas) 100%) !important;
}

.main .block-container {
    max-width: 1200px !important;
    padding: 1.5rem 2rem 4rem 2rem !important;
}

/* ─── Hide default Streamlit sidebar completely ───────────────────── */
[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   BUTTONS  —  Flat & Minimalist (Secondary = Outline, Primary = Solid)
   ═══════════════════════════════════════════════════════════════════════ */

/* Default/Secondary button (Flat Outline) */
.stButton > button, .stDownloadButton > button {
    background: #FFFFFF !important;
    color: var(--text-secondary) !important;
    border: 1px solid rgba(19, 31, 45, 0.12) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.2rem !important;
    font-weight: 500 !important;
    font-family: var(--font) !important;
    box-shadow: none !important;
    transition: none !important;
    cursor: pointer;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: rgba(35, 67, 106, 0.05) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
    box-shadow: none !important;
}
.stButton > button:active, .stDownloadButton > button:active {
    background: rgba(35, 67, 106, 0.10) !important;
    border-color: var(--accent-dark) !important;
}
.stButton > button:focus, .stDownloadButton > button:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(35, 67, 106, 0.10) !important;
}

/* Primary Button (Solid Accent) */
.stButton > button[kind="primary"],
.stButton > button[data-testid*="primary"] {
    background: var(--accent) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--accent) !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid*="primary"]:hover {
    background: var(--accent-light) !important;
    border-color: var(--accent-light) !important;
    color: #FFFFFF !important;
}
.stButton > button[kind="primary"]:active,
.stButton > button[data-testid*="primary"]:active {
    background: var(--accent-dark) !important;
    border-color: var(--accent-dark) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   INPUTS  —  Flat & clean white inputs with thin borders
   ═══════════════════════════════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 1px solid rgba(19, 31, 45, 0.12) !important;
    border-radius: 10px !important;
    padding: 0.6rem 0.8rem !important;
    box-shadow: none !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    transition: none !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div:focus-within {
    outline: none !important;
    border: 1px solid var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(35, 67, 106, 0.10) !important;
}

/* Labels */
.stTextInput label, .stNumberInput label,
.stTextArea label, .stSelectbox label,
.stMultiSelect label, .stSlider label {
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}

/* Fix Dropdown Menus */
[data-baseweb="popover"] {
    background-color: var(--surface) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
}
[data-baseweb="menu"] {
    background-color: transparent !important;
}
ul[role="listbox"] li {
    color: var(--text-primary) !important;
    background-color: transparent !important;
    font-weight: 500 !important;
}
ul[role="listbox"] li[aria-selected="true"] {
    color: var(--accent) !important;
    background-color: var(--bg-canvas) !important;
    font-weight: 700 !important;
}
ul[role="listbox"] li:hover {
    background-color: rgba(35, 67, 106, 0.08) !important;
}

/* Multiselect container */
.stMultiSelect > div {
    background: #FFFFFF !important;
    border-radius: 10px !important;
    border: 1px solid rgba(19, 31, 45, 0.12) !important;
    box-shadow: none !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   CARDS  —  Flat panels with 1px border outlines
   ═══════════════════════════════════════════════════════════════════════ */

/* Diagnostic Card */
.diagnostic-card-glass {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    padding: 22px !important;
    box-shadow: none !important;
    margin-bottom: 1.4rem !important;
}

/* Sunken Card / Input Card */
.medical-input-sunken {
    background: #FFFFFF !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: none !important;
    color: var(--text-primary) !important;
    margin-bottom: 1.4rem !important;
}

/* Metric Card */
.metric-card {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    padding: 1.4rem 1.2rem !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    box-shadow: none !important;
    transition: none !important;
    text-align: center !important;
}
.metric-card:hover {
    box-shadow: none !important;
    border-color: var(--accent) !important;
}
.metric-card .metric-icon {
    font-size: 2rem !important; margin-bottom: 0.45rem !important;
}
.metric-card .metric-value {
    font-size: 2rem !important; font-weight: 800 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.03em; line-height: 1.1;
}
.metric-card .metric-label {
    font-size: 0.78rem !important; color: var(--text-muted) !important;
    font-weight: 700 !important; margin-top: 0.3rem !important;
    text-transform: uppercase !important; letter-spacing: 0.06em !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   PAGE HEADER  —  Flat white block
   ═══════════════════════════════════════════════════════════════════════ */
.page-header {
    background: #FFFFFF !important;
    padding: 1.2rem 1.5rem !important;
    margin-bottom: 1.5rem !important;
    border-radius: 16px !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    box-shadow: none !important;
}
.page-header h1 {
    font-size: 1.8rem !important; font-weight: 800 !important;
    margin: 0 0 0.25rem 0 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.03em;
}
.page-header p {
    margin: 0 !important; font-size: 0.95rem !important;
    color: var(--text-muted) !important; font-weight: 500 !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   SEVERITY BADGES
   ═══════════════════════════════════════════════════════════════════════ */
.severity-badge {
    display: inline-flex !important; align-items: center !important; gap: 0.4rem !important;
    padding: 0.3rem 0.8rem !important; border-radius: 999px !important;
    font-size: 0.78rem !important; font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    background: #FFFFFF !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    box-shadow: none !important;
}
.badge-low      { color: var(--success) !important; }
.badge-moderate { color: var(--warning) !important; }
.badge-high     { color: var(--danger) !important; }
.badge-critical { color: #991B1B; }

/* ═══════════════════════════════════════════════════════════════════════
   TABS  —  Flat outline segments
   ═══════════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.8rem; background: transparent;
    border-bottom: none; padding: 0; margin-bottom: 1rem;
}
.stTabs [data-baseweb="tab"] {
    background: #FFFFFF !important;
    border-radius: 10px !important;
    font-weight: 600; font-family: var(--font);
    color: var(--text-muted) !important;
    padding: 0.6rem 1.2rem !important;
    border: 1px solid rgba(22, 163, 74, 0.12) !important;
    box-shadow: none !important;
    transition: none !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(35, 67, 106, 0.08) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   EXPANDERS  —  Flat panels
   ═══════════════════════════════════════════════════════════════════════ */
.streamlit-expanderHeader {
    font-weight: 600 !important; font-family: var(--font) !important;
    font-size: 0.95rem !important; color: var(--text-primary) !important;
}
details {
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    border-radius: 12px !important;
    background: #FFFFFF !important;
    box-shadow: none !important;
    margin-bottom: 0.8rem !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   PROGRESS BAR
   ═══════════════════════════════════════════════════════════════════════ */
.stProgress > div > div > div > div {
    background-color: var(--accent) !important;
    border-radius: 999px !important;
}
.stProgress > div > div {
    border-radius: 999px !important;
    box-shadow: none !important;
    background: rgba(35, 67, 106, 0.08) !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   DISCLAIMER BANNER
   ═══════════════════════════════════════════════════════════════════════ */
.disclaimer-banner {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    padding: 1rem 1.4rem !important;
    font-size: 0.82rem !important; color: var(--text-muted) !important;
    line-height: 1.6 !important; margin-bottom: 1.2rem !important;
    box-shadow: none !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    border-left: 4px solid var(--warning) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   WIZARD PROGRESS  —  Flat row
   ═══════════════════════════════════════════════════════════════════════ */
.wizard-steps {
    display: flex !important; align-items: center !important; gap: 0 !important;
    margin-bottom: 1.8rem !important;
    background: #FFFFFF !important;
    padding: 0.8rem 1rem !important;
    border-radius: 16px !important;
    border: 1px solid rgba(22, 163, 74, 0.12) !important;
    box-shadow: none !important;
}
.wizard-step {
    display: flex !important; align-items: center !important;
    gap: 0.5rem !important; flex: 1 !important;
    justify-content: center !important;
}
.wizard-step .step-circle {
    width: 28px !important; height: 28px !important;
    border-radius: 50% !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    font-size: 0.85rem !important; font-weight: 700 !important;
    flex-shrink: 0 !important;
    background: #FFFFFF !important;
    color: var(--text-muted) !important;
    border: 1px solid rgba(19, 31, 45, 0.12) !important;
    box-shadow: none !important;
    transition: none !important;
}
.wizard-step .step-label {
    font-size: 0.82rem !important; font-weight: 600 !important;
    white-space: nowrap !important; color: var(--text-muted) !important;
}
.wizard-step.active .step-circle {
    background: var(--accent) !important; color: #FFFFFF !important;
    border-color: var(--accent) !important;
    box-shadow: none !important;
}
.wizard-step.active .step-label { color: var(--accent) !important; }
.wizard-step.completed .step-circle {
    background: var(--success) !important; color: #FFFFFF !important;
    border-color: var(--success) !important;
    box-shadow: none !important;
}
.wizard-step.completed .step-label { color: var(--success) !important; }

.wizard-connector {
    flex: 0.4 !important; height: 2px !important;
    background: rgba(35, 67, 106, 0.10) !important;
    box-shadow: none !important;
    margin: 0 0.4rem !important; border-radius: 1px !important;
}
.wizard-connector.completed {
    background: var(--success) !important;
    box-shadow: none !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   ANIMATIONS DISABLED
   ═══════════════════════════════════════════════════════════════════════ */
.animate-in {
    animation: none !important;
}
[class*="animate-in-"] {
    animation: none !important;
    animation-delay: 0s !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   ADDITIONAL STREAMLIT CONTAINERS
   ═══════════════════════════════════════════════════════════════════════ */

/* Plotly charts container */
.stPlotlyChart {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    padding: 0.8rem !important;
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    box-shadow: none !important;
    margin-bottom: 1rem !important;
}

/* Slider */
.stSlider > div > div {
    padding: 0.5rem 0 !important;
}
.stSlider [data-baseweb="slider"] {
    margin-top: 0.5rem;
}

/* Horizontal dividers */
hr {
    border: none !important;
    height: 1px !important;
    background: rgba(35, 67, 106, 0.10) !important;
    box-shadow: none !important;
    margin: 1.5rem 0 !important;
}

/* Alert / info / warning boxes */
.stAlert {
    border: 1px solid rgba(19, 31, 45, 0.10) !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
"""
