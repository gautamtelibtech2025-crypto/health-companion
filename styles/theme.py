"""
HealthAI Pro — Light Green 3D Skeuomorphic UI Engine

Every element is rendered with physical 3D depth — raised buttons pop out
of the surface, inputs are carved inward, and all interactive elements
respond with tactile press/release animations.
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
      rel="stylesheet">
"""

# ─── Master CSS ───────────────────────────────────────────────────────────────

_CSS: str = """
/* ═══════════════════════════════════════════════════════════════════════
   HEALTHAI PRO — LIGHT GREEN 3D SKEUOMORPHIC THEME
   Light source: top-left (315°).  Everything is tactile & physical.
   ═══════════════════════════════════════════════════════════════════════ */

:root {
  /* ── Color Palette ─────────────────────────────────────────────── */
  --bg-canvas: #E8EFE8;              /* Soft sage-mint canvas */
  --surface: #F2F7F2;                /* White-green for raised 3D elements */
  --text-primary: #1A2E1A;           /* Deep forest text */
  --text-secondary: #3D5A3D;         /* Medium green-gray */
  --text-muted: #6B8A6B;             /* Faded green for labels */
  --accent: #16A34A;                 /* Vibrant green — primary accent */
  --accent-light: #22C55E;
  --accent-dark: #15803D;
  --success: #22C55E;
  --warning: #EAB308;
  --danger: #DC2626;
  --info: #2563EB;

  /* ── 3D Shadow Matrix (Top-Left Light Source) ──────────────────── */
  --shadow-raised:
    -6px -6px 14px 0px rgba(255, 255, 255, 0.85),
     6px  6px 14px 0px rgba(140, 160, 140, 0.30);

  --shadow-raised-hover:
    -8px -8px 20px 0px rgba(255, 255, 255, 0.95),
     8px  8px 20px 0px rgba(140, 160, 140, 0.40);

  --shadow-pressed:
    inset -3px -3px 7px 0px rgba(255, 255, 255, 0.80),
    inset  3px  3px 7px 0px rgba(140, 160, 140, 0.35);

  --shadow-sunken:
    inset -4px -4px 10px 0px rgba(255, 255, 255, 0.85),
    inset  4px  4px 10px 0px rgba(140, 160, 140, 0.30);

  /* ── Glassmorphism (used sparingly on top of solid surfaces) ──── */
  --glass-bg: rgba(242, 247, 242, 0.50);
  --glass-border: 1px solid rgba(255, 255, 255, 0.70);
  --glass-blur: blur(20px) saturate(180%);

  /* ── Misc ──────────────────────────────────────────────────────── */
  --transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  --font: 'Inter', sans-serif;
}

/* ─── Global ────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    color: var(--text-primary);
    background-color: var(--bg-canvas) !important;
}

.stApp { background: var(--bg-canvas) !important; }

.main .block-container {
    max-width: 1100px;
    padding: 2rem 2rem 4rem 2rem !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   SIDEBAR  —  Central Navigation Hub
   ═══════════════════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--bg-canvas) !important;
    border-right: none !important;
    box-shadow: 4px 0 18px rgba(140, 160, 140, 0.12) !important;
}

/* Brand */
section[data-testid="stSidebar"] .stMarkdown h1 {
    font-size: 1.45rem !important; font-weight: 800 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em; margin-bottom: 0 !important;
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: var(--accent) !important;
    font-size: 0.82rem !important; font-weight: 600 !important;
    margin-top: 2px !important;
}

/* Nav buttons — 3D raised pills */
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    text-align: left !important; justify-content: flex-start !important;
    background: var(--surface) !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.85rem 1.15rem !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    color: var(--text-secondary) !important;
    box-shadow: var(--shadow-raised) !important;
    transition: var(--transition) !important;
    margin-bottom: 10px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    color: var(--accent) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-raised-hover) !important;
}
section[data-testid="stSidebar"] .stButton > button:active {
    transform: translateY(2px) !important;
    box-shadow: var(--shadow-pressed) !important;
    color: var(--accent-dark) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   BUTTONS  —  Every button is a physical 3D object
   ═══════════════════════════════════════════════════════════════════════ */
.stButton > button {
    background: var(--surface) !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.6rem !important;
    border-radius: 16px !important;
    border: none !important;
    box-shadow: var(--shadow-raised) !important;
    transition: var(--transition) !important;
    cursor: pointer;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-raised-hover) !important;
    color: var(--accent) !important;
}
.stButton > button:active {
    transform: translateY(2px) !important;
    box-shadow: var(--shadow-pressed) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   INPUTS  —  Carved / sunken into the surface
   ═══════════════════════════════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg-canvas) !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 1rem !important;
    box-shadow: var(--shadow-sunken) !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    transition: var(--transition) !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div:focus-within {
    outline: none !important;
    border: 1px solid rgba(22, 163, 74, 0.45) !important;
    box-shadow: var(--shadow-sunken), 0 0 0 2px rgba(22, 163, 74, 0.12) !important;
}

/* Labels */
.stTextInput label, .stNumberInput label,
.stTextArea label, .stSelectbox label,
.stMultiSelect label, .stSlider label {
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}

/* Fix Dropdown Menus (Selectbox/Multiselect) visibility */
[data-baseweb="popover"] {
    background-color: var(--surface) !important;
    border-radius: 14px !important;
    box-shadow: var(--shadow-raised) !important;
    border: none !important;
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
    background-color: rgba(22, 163, 74, 0.08) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   CARDS
   ═══════════════════════════════════════════════════════════════════════ */

/* Glass Card (for diagnostic results / insights) */
.diagnostic-card-glass {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-radius: 24px;
    border: var(--glass-border);
    padding: 22px;
    box-shadow: 0 8px 30px rgba(140, 160, 140, 0.10);
    position: relative; overflow: hidden;
    margin-bottom: 1.4rem;
}
.diagnostic-card-glass::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 40%;
    background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0) 100%);
    pointer-events: none; border-radius: 24px 24px 0 0;
}

/* Sunken Card (for graphs / inputs) */
.medical-input-sunken {
    background: var(--bg-canvas);
    border: none;
    border-radius: 20px;
    padding: 20px;
    box-shadow: var(--shadow-sunken);
    color: var(--text-primary);
    margin-bottom: 1.4rem;
}

/* ═══════════════════════════════════════════════════════════════════════
   METRIC CARDS  —  Raised 3D tiles
   ═══════════════════════════════════════════════════════════════════════ */
.metric-card {
    background: var(--surface);
    border-radius: 20px;
    padding: 1.4rem 1.2rem;
    border: none;
    box-shadow: var(--shadow-raised);
    transition: var(--transition);
    text-align: center;
    position: relative; overflow: hidden;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-raised-hover);
}
.metric-card .metric-icon {
    font-size: 2rem; margin-bottom: 0.45rem;
}
.metric-card .metric-value {
    font-size: 2rem; font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em; line-height: 1.1;
}
.metric-card .metric-label {
    font-size: 0.78rem; color: var(--text-muted);
    font-weight: 700; margin-top: 0.3rem;
    text-transform: uppercase; letter-spacing: 0.06em;
}

/* ═══════════════════════════════════════════════════════════════════════
   PAGE HEADER  —  Raised 3D block
   ═══════════════════════════════════════════════════════════════════════ */
.page-header {
    background: var(--surface);
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.8rem;
    border-radius: 20px;
    box-shadow: var(--shadow-raised);
}
.page-header h1 {
    font-size: 2rem; font-weight: 800;
    margin: 0 0 0.35rem 0;
    color: var(--text-primary) !important;
    letter-spacing: -0.03em;
}
.page-header p {
    margin: 0; font-size: 1rem;
    color: var(--text-muted); font-weight: 500;
}

/* ═══════════════════════════════════════════════════════════════════════
   SEVERITY BADGES  —  Small raised pills
   ═══════════════════════════════════════════════════════════════════════ */
.severity-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.3rem 0.8rem; border-radius: 999px;
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 0.02em;
    background: var(--surface);
    box-shadow: var(--shadow-raised);
}
.badge-low      { color: var(--success); }
.badge-moderate { color: var(--warning); }
.badge-high     { color: var(--danger); }
.badge-critical { color: #991B1B; }

/* ═══════════════════════════════════════════════════════════════════════
   TABS  —  3D Raised Segments
   ═══════════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.8rem; background: transparent;
    border-bottom: none; padding: 0; margin-bottom: 1rem;
}
.stTabs [data-baseweb="tab"] {
    background: var(--surface);
    border-radius: 14px;
    font-weight: 600; font-family: var(--font);
    color: var(--text-muted);
    padding: 0.7rem 1.3rem;
    border: none;
    box-shadow: var(--shadow-raised);
    transition: var(--transition);
}
.stTabs [aria-selected="true"] {
    background: var(--bg-canvas) !important;
    color: var(--accent) !important;
    box-shadow: var(--shadow-pressed) !important;
    transform: translateY(2px);
}

/* ═══════════════════════════════════════════════════════════════════════
   EXPANDERS  —  Raised 3D panels
   ═══════════════════════════════════════════════════════════════════════ */
.streamlit-expanderHeader {
    font-weight: 600 !important; font-family: var(--font) !important;
    font-size: 0.95rem !important; color: var(--text-primary) !important;
}
details {
    border: none !important;
    border-radius: 18px !important;
    background: var(--surface) !important;
    box-shadow: var(--shadow-raised) !important;
    margin-bottom: 0.8rem !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   PROGRESS BAR  —  Sunken track + raised fill
   ═══════════════════════════════════════════════════════════════════════ */
.stProgress > div > div > div > div {
    background-color: var(--accent) !important;
    border-radius: 999px !important;
}
.stProgress > div > div {
    border-radius: 999px !important;
    box-shadow: var(--shadow-sunken) !important;
    background: var(--bg-canvas) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   DISCLAIMER BANNER
   ═══════════════════════════════════════════════════════════════════════ */
.disclaimer-banner {
    background: var(--surface);
    border-radius: 18px;
    padding: 1rem 1.4rem;
    font-size: 0.82rem; color: var(--text-muted);
    line-height: 1.6; margin-bottom: 1.2rem;
    box-shadow: var(--shadow-raised);
    border-left: 4px solid var(--warning);
}

/* ═══════════════════════════════════════════════════════════════════════
   WIZARD PROGRESS  —  Sunken track + raised step circles
   ═══════════════════════════════════════════════════════════════════════ */
.wizard-steps {
    display: flex; align-items: center; gap: 0;
    margin-bottom: 2.2rem;
    background: var(--bg-canvas);
    padding: 0.9rem 1rem;
    border-radius: 22px;
    box-shadow: var(--shadow-sunken);
}
.wizard-step {
    display: flex; align-items: center;
    gap: 0.5rem; flex: 1;
    justify-content: center;
}
.wizard-step .step-circle {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700;
    flex-shrink: 0;
    background: var(--surface);
    color: var(--text-muted);
    box-shadow: var(--shadow-raised);
    transition: var(--transition);
}
.wizard-step .step-label {
    font-size: 0.82rem; font-weight: 600;
    white-space: nowrap; color: var(--text-muted);
}
.wizard-step.active .step-circle {
    background: var(--bg-canvas); color: var(--accent);
    box-shadow: var(--shadow-pressed);
}
.wizard-step.active .step-label { color: var(--accent); }
.wizard-step.completed .step-circle {
    background: var(--bg-canvas); color: var(--success);
    box-shadow: var(--shadow-pressed);
}
.wizard-step.completed .step-label { color: var(--success); }

.wizard-connector {
    flex: 0.4; height: 4px;
    background: var(--bg-canvas);
    box-shadow: var(--shadow-sunken);
    margin: 0 0.4rem; border-radius: 2px;
}
.wizard-connector.completed {
    background: var(--accent-light);
    box-shadow: none;
}

/* ═══════════════════════════════════════════════════════════════════════
   ANIMATIONS
   ═══════════════════════════════════════════════════════════════════════ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeInUp 0.35s ease-out both; }
.animate-in-1 { animation-delay: 0.05s; }
.animate-in-2 { animation-delay: 0.10s; }
.animate-in-3 { animation-delay: 0.15s; }
.animate-in-4 { animation-delay: 0.20s; }

/* ─── Hide default Streamlit chrome ─────────────────────────────────── */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }

/* Hide the auto-generated page navigation in the sidebar */
[data-testid="stSidebarNav"] { display: none !important; }
nav[data-testid="stSidebarNav"] { display: none !important; }
ul[data-testid="stSidebarNavItems"] { display: none !important; }

/* ═══════════════════════════════════════════════════════════════════════
   EVERYTHING 3D — Native Streamlit containers
   ═══════════════════════════════════════════════════════════════════════ */

/* Plotly charts container */
.stPlotlyChart {
    background: var(--surface);
    border-radius: 20px;
    padding: 0.8rem;
    box-shadow: var(--shadow-raised);
    margin-bottom: 1rem;
}

/* Multiselect */
.stMultiSelect > div {
    background: var(--bg-canvas) !important;
    border-radius: 14px !important;
    box-shadow: var(--shadow-sunken) !important;
    border: none !important;
}

/* Slider */
.stSlider > div > div {
    padding: 0.5rem 0 !important;
}
.stSlider [data-baseweb="slider"] {
    margin-top: 0.5rem;
}

/* Download button */
.stDownloadButton > button {
    background: var(--surface) !important;
    border: none !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow-raised) !important;
    font-weight: 600 !important;
    transition: var(--transition) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-raised-hover) !important;
    color: var(--accent) !important;
}
.stDownloadButton > button:active {
    transform: translateY(2px) !important;
    box-shadow: var(--shadow-pressed) !important;
}

/* Horizontal dividers */
hr {
    border: none !important;
    height: 3px !important;
    background: var(--bg-canvas) !important;
    box-shadow: var(--shadow-sunken) !important;
    border-radius: 2px !important;
    margin: 1.5rem 0 !important;
}

/* Alert / info / warning boxes */
.stAlert {
    border: none !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow-raised) !important;
}
"""
