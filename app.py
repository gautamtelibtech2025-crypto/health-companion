"""
HealthAI Pro — Main Application Entry Point

Run with: streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from config.settings import APP_ICON, APP_NAME, get_gemini_api_key
from styles.theme import inject_theme
from components.sidebar import render_sidebar
from services.gemini_service import GeminiService

# ─── Page Config (must be the first Streamlit call) ───────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inject Premium Theme ────────────────────────────────────────────────────
inject_theme()

# ─── Session State Initialization ─────────────────────────────────────────────
_DEFAULTS: dict = {
    "current_page": "dashboard",
    "wizard_step": 1,
    "assessment_data": {},
    "last_analysis": None,
    "run_analysis": False,
    "manual_api_key": "",
    "confirm_delete_all": False,
}

for key, default in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Auto-configure Gemini from env if available ──────────────────────────────
if not GeminiService.is_configured():
    env_key = get_gemini_api_key()
    if env_key:
        GeminiService.configure(env_key)
    elif st.session_state.get("manual_api_key"):
        GeminiService.configure(st.session_state["manual_api_key"])

# ─── Sidebar Navigation ──────────────────────────────────────────────────────
current_page = render_sidebar()

# ─── Page Router ──────────────────────────────────────────────────────────────
if current_page == "dashboard":
    from views.dashboard import render_dashboard
    render_dashboard()

elif current_page == "assessment":
    from views.assessment import render_assessment
    render_assessment()

elif current_page == "analysis":
    from views.analysis import render_analysis
    render_analysis()

elif current_page == "reports":
    from views.reports import render_reports
    render_reports()

elif current_page == "settings":
    from views.settings_page import render_settings
    render_settings()

else:
    from views.dashboard import render_dashboard
    render_dashboard()
