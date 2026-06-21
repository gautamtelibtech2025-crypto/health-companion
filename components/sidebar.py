"""
HealthAI Pro — Sidebar Navigation Component

Prominent sidebar with 3D raised nav buttons and all options visible.
"""

from __future__ import annotations

import streamlit as st

from config.settings import APP_NAME, APP_VERSION, NAV_ITEMS, DISCLAIMER


def render_sidebar() -> str:
    """Render the sidebar navigation and return the selected page key."""
    with st.sidebar:
        # ── Branding ──────────────────────────────────────────────
        st.markdown(
            f"""
            <div style="padding:0.6rem 0 1rem 0;text-align:left;">
                <div style="font-size:2.2rem;margin-bottom:0.15rem;">🏥</div>
                <h1 style="margin:0;">{APP_NAME}</h1>
                <p style="margin:0;">v{APP_VERSION} · AI Health Assistant</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Section heading
        st.markdown(
            '<div style="font-size:0.72rem;color:var(--text-muted);font-weight:700;'
            'text-transform:uppercase;letter-spacing:0.1em;margin:1rem 0 0.7rem 0;'
            'padding-bottom:0.4rem;border-bottom:2px solid rgba(22,163,74,0.12);">'
            '🧭 Navigation</div>',
            unsafe_allow_html=True,
        )

        # ── Navigation Items ──────────────────────────────────────
        current = st.session_state.get("current_page", "dashboard")

        for item in NAV_ITEMS:
            key = item["key"]
            label = f"{item['icon']}  {item['label']}"

            if key == current:
                # Active page → pressed/sunken 3D look + green accent
                st.markdown(
                    f"""
                    <div style="
                        background: var(--bg-canvas);
                        border-radius: 16px;
                        padding: 0.85rem 1.15rem;
                        margin-bottom: 10px;
                        box-shadow: var(--shadow-pressed);
                        border-left: 3px solid var(--accent);
                    ">
                        <span style="font-weight:700;color:var(--accent);font-size:0.95rem;">
                            {label}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                # Inactive → 3D raised button (CSS handles hover/active)
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.session_state["current_page"] = key
                    st.rerun()

        # ── Bottom ────────────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            """
            <div style="font-size:0.72rem;color:var(--text-muted);line-height:1.55;">
                ⚕️ <strong>Disclaimer</strong>: AI-generated health info for
                educational purposes only. Not a substitute for professional
                medical advice.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return current
