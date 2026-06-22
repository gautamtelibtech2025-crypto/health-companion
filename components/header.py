"""
Health Companion — Page Header Component

Simple section header for each page.
"""

from __future__ import annotations

import re
import streamlit as st
import textwrap


def page_header(title: str, subtitle: str = "", icon: str = "") -> None:
    """Render a simple page header with optional icon and subtitle.

    Args:
        title: Main heading text.
        subtitle: Optional description line.
        icon: Optional emoji/icon displayed before the title.
    """
    clean_title = re.sub(r"^[^\w]+\s*", "", title)
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""

    st.markdown(
        textwrap.dedent(
            f"""
            <div class="page-header animate-in">
                <h1>{clean_title}</h1>
                {subtitle_html}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
