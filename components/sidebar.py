"""
HealthAI Pro — Sidebar Navigation Component

Custom branded sidebar with icon-based navigation and active-state highlighting.
"""

from __future__ import annotations

import streamlit as st

from config.settings import APP_NAME, APP_VERSION, NAV_ITEMS, DISCLAIMER


def render_sidebar() -> str:
    """Render the sidebar navigation and return the selected page key.

    Returns:
        The key string of the selected page (e.g. 'dashboard', 'assessment').
    """
    with st.sidebar:
        # ── Branding ──────────────────────────────────────────────
        st.markdown(
            f"""
            <div style="padding:0.8rem 0 1.2rem 0;text-align:center;">
                <div style="font-size:2.4rem;margin-bottom:0.3rem;">🏥</div>
                <h1 style="margin:0;">{APP_NAME}</h1>
                <p style="margin:0.2rem 0 0 0;">v{APP_VERSION} · AI Health Assistant</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ── Navigation Items ──────────────────────────────────────
        current = st.session_state.get("current_page", "dashboard")

        for item in NAV_ITEMS:
            key = item["key"]
            label = f"{item['icon']}  {item['label']}"

            # Highlight active page
            if key == current:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(14,165,233,0.1), rgba(139,92,246,0.08));
                        border-radius: 14px;
                        padding: 0.7rem 1rem;
                        margin-bottom: 4px;
                        border-left: 3px solid #0EA5E9;
                    ">
                        <span style="font-weight:600;color:#0EA5E9;font-size:0.92rem;">{label}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.session_state["current_page"] = key
                    st.rerun()

        # ── Bottom section ────────────────────────────────────────
        st.markdown("---")

        # Compact disclaimer
        st.markdown(
            """
            <div style="
                font-size:0.72rem;
                color:#94A3B8;
                line-height:1.5;
                padding:0 0.2rem;
            ">
                ⚕️ <strong>Disclaimer</strong>: This tool provides AI-generated
                health information for educational purposes only. It is not a
                substitute for professional medical advice.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return current
