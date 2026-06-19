"""
HealthAI Pro — Settings Page

API key configuration, connection testing, and data management.
"""

from __future__ import annotations

import streamlit as st

from components.header import page_header
from components.cards import glass_card, neu_card
from config.settings import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    GEMINI_MODEL,
    get_gemini_api_key,
)
from services.gemini_service import GeminiService
from services.report_store import ReportStore


def render_settings() -> None:
    """Render the Settings page."""

    page_header(
        title="Settings",
        subtitle="Configure your API key and manage application data.",
        icon="⚙️",
    )

    # ── Gemini API Key ────────────────────────────────────────────
    glass_card(
        title="🔑 Gemini API Configuration",
        content="""
        <p style="color:#475569;font-size:0.88rem;line-height:1.6;">
            Enter your Google Gemini API key to enable AI analysis.
            The key is stored in your session only and is never persisted to disk.
            You can also set the <code>GEMINI_API_KEY</code> environment variable.
        </p>
        """,
        animation_index=1,
    )

    # Check env var
    env_key = get_gemini_api_key()
    if env_key:
        st.markdown(
            """
            <div class="neu-card" style="border-left:3px solid #22C55E;padding:0.8rem 1rem;">
                <span style="font-size:0.85rem;color:#22C55E;font-weight:600;">
                    ✅ API key detected from environment variable <code>GEMINI_API_KEY</code>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if not GeminiService.is_configured():
            GeminiService.configure(env_key)

    # Manual input
    current_key = st.session_state.get("manual_api_key", "")
    api_key = st.text_input(
        "Gemini API Key",
        value=current_key,
        type="password",
        placeholder="Enter your API key here...",
        key="api_key_input",
        help="Get your API key from https://aistudio.google.com/apikey",
    )

    # Model Selection Dropdown
    model_options = [
        "gemini-2.5-flash",
        "gemini-flash-latest",
        "gemini-3.5-flash",
        "gemini-2.0-flash",
        "gemini-pro-latest",
        "gemini-2.5-pro",
    ]
    current_model = st.session_state.get("selected_model", GEMINI_MODEL)
    if current_model not in model_options:
        model_options.append(current_model)

    selected_model = st.selectbox(
        "Active Gemini Model",
        options=model_options,
        index=model_options.index(current_model),
        help="Select which Gemini model to use for health assessments. If you encounter quota/rate limits (e.g. 429 errors) on gemini-2.0-flash, switching to gemini-2.5-flash or gemini-flash-latest (which maps to 1.5-flash) will solve the issue.",
    )
    if selected_model != current_model:
        st.session_state["selected_model"] = selected_model
        st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾  Save API Key", key="save_key", use_container_width=True):
            if api_key.strip():
                st.session_state["manual_api_key"] = api_key.strip()
                GeminiService.configure(api_key.strip())
                st.success("✅ API key saved and configured!")
            else:
                st.warning("Please enter a valid API key.")

    with col2:
        if st.button("🔌  Test Connection", key="test_conn", use_container_width=True):
            # Configure first if key is available but not configured
            if not GeminiService.is_configured():
                key_to_use = api_key.strip() or env_key
                if key_to_use:
                    GeminiService.configure(key_to_use)

            if GeminiService.is_configured():
                with st.spinner("Testing connection..."):
                    success, message = GeminiService.test_connection()
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("No API key available. Enter a key or set the environment variable.")

    # ── Connection Status ─────────────────────────────────────────
    status_color = "#22C55E" if GeminiService.is_configured() else "#EF4444"
    status_text = "Connected" if GeminiService.is_configured() else "Not Connected"
    status_icon = "🟢" if GeminiService.is_configured() else "🔴"

    st.markdown(
        f"""
        <div class="neu-card" style="padding:1rem;margin-top:0.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-size:0.82rem;color:#94A3B8;text-transform:uppercase;
                        letter-spacing:0.05em;">Connection Status</span>
                    <div style="font-size:1rem;font-weight:600;color:{status_color};margin-top:0.15rem;">
                        {status_icon} {status_text}
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:0.82rem;color:#94A3B8;">Model</span>
                    <div style="font-size:0.9rem;font-weight:500;color:#0F172A;">{GeminiService.get_model_name()}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # ── Data Management ───────────────────────────────────────────
    glass_card(
        title="🗂️ Data Management",
        content="""
        <p style="color:#475569;font-size:0.88rem;line-height:1.6;">
            Manage your locally stored health assessment reports.
            All data is stored on your machine in the <code>reports/</code> folder.
        </p>
        """,
        animation_index=2,
    )

    store = ReportStore()
    count = store.report_count()

    st.markdown(
        f"""
        <div class="neu-card" style="padding:1rem;">
            <span style="font-size:0.82rem;color:#94A3B8;text-transform:uppercase;
                letter-spacing:0.05em;">Stored Reports</span>
            <div style="font-size:1.8rem;font-weight:800;color:#0F172A;margin-top:0.15rem;">
                {count}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if count > 0:
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        if st.button("🗑️  Delete All Reports", key="delete_all", use_container_width=True):
            st.session_state["confirm_delete_all"] = True

        if st.session_state.get("confirm_delete_all"):
            st.warning("⚠️ This will permanently delete all reports and PDFs. This cannot be undone.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Yes, delete all", key="confirm_del_yes", use_container_width=True):
                    deleted = store.delete_all_reports()
                    st.session_state["confirm_delete_all"] = False
                    st.success(f"Deleted {deleted} reports.")
                    st.rerun()
            with c2:
                if st.button("❌ Cancel", key="confirm_del_no", use_container_width=True):
                    st.session_state["confirm_delete_all"] = False
                    st.rerun()

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # ── About ─────────────────────────────────────────────────────
    glass_card(
        title="ℹ️ About",
        content=f"""
        <table style="width:100%;font-size:0.88rem;color:#475569;">
            <tr><td style="padding:0.3rem 0;font-weight:600;width:35%;">Application</td>
                <td>{APP_NAME}</td></tr>
            <tr><td style="padding:0.3rem 0;font-weight:600;">Version</td>
                <td>{APP_VERSION}</td></tr>
            <tr><td style="padding:0.3rem 0;font-weight:600;">AI Model</td>
                <td>{GeminiService.get_model_name()}</td></tr>
            <tr><td style="padding:0.3rem 0;font-weight:600;">Frontend</td>
                <td>Streamlit</td></tr>
            <tr><td style="padding:0.3rem 0;font-weight:600;">PDF Engine</td>
                <td>ReportLab</td></tr>
            <tr><td style="padding:0.3rem 0;font-weight:600;">Charts</td>
                <td>Plotly</td></tr>
        </table>
        <p style="color:#94A3B8;font-size:0.82rem;margin-top:0.8rem;margin-bottom:0;">
            {APP_DESCRIPTION}
        </p>
        """,
        animation_index=3,
    )
