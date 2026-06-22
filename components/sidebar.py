"""
HealthAI Pro — Top Navigation Component

Horizontal navigation header with flat outline nav buttons.
"""

from __future__ import annotations

import streamlit as st
import textwrap

from config.settings import APP_NAME, APP_VERSION, NAV_ITEMS


def render_sidebar() -> str:
    """Render horizontal navigation at the top of the page."""
    col_brand, col_nav = st.columns([1, 2])

    with col_brand:
        st.markdown(
            textwrap.dedent(
                f"""
                <div style="display:flex;align-items:center;gap:0.65rem;padding:0.4rem 0;">
                    <span style="width:0.9rem;height:0.9rem;border-radius:999px;background:var(--accent);display:inline-block;"></span>
                    <div>
                        <h1 style="margin:0;font-size:1.35rem;font-weight:700;color:var(--text-primary);line-height:1.1;letter-spacing:-0.02em;">{APP_NAME}</h1>
                        <p style="margin:0;font-size:0.78rem;font-weight:500;color:var(--text-muted);line-height:1;">v{APP_VERSION} · simple health notes</p>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with col_nav:
        current = st.session_state.get("current_page", "dashboard")
        # Layout columns for buttons
        nav_cols = st.columns(len(NAV_ITEMS))
        for idx, item in enumerate(NAV_ITEMS):
            key = item["key"]
            label = item["label"]
            with nav_cols[idx]:
                if key == current:
                    st.markdown(
                        textwrap.dedent(
                            f"""
                            <div style="
                                background: rgba(35, 67, 106, 0.08);
                                border-radius: 10px;
                                border: 1px solid rgba(35, 67, 106, 0.24);
                                padding: 0.6rem 0.35rem;
                                text-align: center;
                                margin-top: 0.2rem;
                            ">
                                <span style="font-weight:600;color:var(--accent);font-size:0.84rem;white-space:nowrap;">
                                    {label}
                                </span>
                            </div>
                            """
                        ),
                        unsafe_allow_html=True,
                    )
                else:
                    if st.button(label, key=f"nav_{key}", use_container_width=True):
                        st.session_state["current_page"] = key
                        st.rerun()

    # Render a clean separator below the navbar
    st.markdown("<hr style='margin:0.45rem 0 1.2rem 0 !important;'>", unsafe_allow_html=True)

    return current
