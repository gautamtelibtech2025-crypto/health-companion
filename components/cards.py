"""
HealthAI Pro — Card Components

Glassmorphism and neumorphic card wrappers for content display.
"""

from __future__ import annotations

import streamlit as st


def glass_card(
    content: str,
    title: str | None = None,
    animation_index: int = 0,
) -> None:
    """Render a frosted-glass card with optional title.

    Args:
        content: Inner HTML/markdown content.
        title: Optional card title rendered as <h3>.
        animation_index: Staggered animation delay index (0–4).
    """
    anim_class = f"animate-in animate-in-{animation_index}" if animation_index else "animate-in"
    title_html = f'<h3 style="margin:0 0 0.75rem 0;font-size:1.05rem;font-weight:600;">{title}</h3>' if title else ""
    st.markdown(
        f"""
        <div class="glass-card {anim_class}">
            {title_html}
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def neu_card(
    content: str,
    title: str | None = None,
    animation_index: int = 0,
) -> None:
    """Render a neumorphic card with soft shadows.

    Args:
        content: Inner HTML/markdown content.
        title: Optional card title rendered as <h3>.
        animation_index: Staggered animation delay index (0–4).
    """
    anim_class = f"animate-in animate-in-{animation_index}" if animation_index else "animate-in"
    title_html = f'<h3 style="margin:0 0 0.75rem 0;font-size:1.05rem;font-weight:600;">{title}</h3>' if title else ""
    st.markdown(
        f"""
        <div class="neu-card {anim_class}">
            {title_html}
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(
    icon: str,
    title: str,
    value: str,
    color: str = "#0EA5E9",
    animation_index: int = 0,
) -> None:
    """Render a compact information card with an icon and single value.

    Args:
        icon: Emoji or icon string.
        title: Card label/title.
        value: Main display value.
        color: Accent color for the top border.
        animation_index: Staggered animation delay index.
    """
    anim_class = f"animate-in animate-in-{animation_index}" if animation_index else "animate-in"
    st.markdown(
        f"""
        <div class="glass-card {anim_class}" style="text-align:center;padding:1.4rem 1rem;
            border-top:3px solid {color};">
            <div style="font-size:2rem;margin-bottom:0.4rem;">{icon}</div>
            <div style="font-size:1.5rem;font-weight:800;color:{color};letter-spacing:-0.02em;">{value}</div>
            <div style="font-size:0.8rem;color:#94A3B8;font-weight:500;text-transform:uppercase;
                letter-spacing:0.05em;margin-top:0.2rem;">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text: str, severity: str = "Low") -> str:
    """Return HTML for a colored severity badge.

    Args:
        text: Badge label text.
        severity: One of 'Low', 'Moderate', 'High', 'Critical'.

    Returns:
        HTML string for the badge (use with st.markdown + unsafe_allow_html).
    """
    css_class = {
        "Low": "badge-low",
        "Moderate": "badge-moderate",
        "High": "badge-high",
        "Critical": "badge-critical",
    }.get(severity, "badge-low")

    icon = {"Low": "🟢", "Moderate": "🟡", "High": "🔴", "Critical": "🚨"}.get(severity, "🟢")

    return f'<span class="severity-badge {css_class}">{icon} {text}</span>'
