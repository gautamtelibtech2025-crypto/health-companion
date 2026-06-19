"""
HealthAI Pro — Page Header Component

Gradient hero-style header for each page.
"""

from __future__ import annotations

import streamlit as st


def page_header(title: str, subtitle: str = "", icon: str = "") -> None:
    """Render a gradient page header with optional icon and subtitle.

    Args:
        title: Main heading text.
        subtitle: Optional description line.
        icon: Optional emoji/icon displayed before the title.
    """
    icon_html = f'<span style="font-size:1.5rem;margin-right:0.5rem;">{icon}</span>' if icon else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""

    st.markdown(
        f"""
        <div class="page-header animate-in">
            <h1>{icon_html}{title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
