"""
HealthAI Pro — Card Components

Glassmorphic and Sunken card wrappers for content display.
"""

from __future__ import annotations

import textwrap
import streamlit as st


def glass_card(
    content: str,
    title: str | None = None,
    animation_index: int = 0,
) -> None:
    """Render a frosted glass diagnostic card with optional title."""
    anim_class = f"animate-in animate-in-{animation_index}" if animation_index else "animate-in"
    header_html = ""
    if title:
        header_html = f'<div class="card-header" style="margin-bottom: 1rem;"><h3 class="metric-title" style="margin:0;font-size:1.15rem;font-weight:700;color:var(--text-primary);">{title}</h3></div>'
        
    content_clean = textwrap.dedent(content).strip()
    full_html = f'<div class="diagnostic-card-glass {anim_class}">\n{header_html}\n{content_clean}\n</div>'
    
    st.markdown(full_html, unsafe_allow_html=True)


def raised_card(
    content: str,
    title: str | None = None,
    animation_index: int = 0,
) -> None:
    """Render a solid 3D raised surface."""
    anim_class = f"animate-in animate-in-{animation_index}" if animation_index else "animate-in"
    title_html = f'<h3 style="margin:0 0 0.75rem 0;font-size:1.1rem;font-weight:600;color:var(--text-primary);">{title}</h3>' if title else ""
    
    content_clean = textwrap.dedent(content).strip()
    full_html = f'<div class="metric-card {anim_class}" style="text-align:left; margin-bottom:1.4rem;">\n{title_html}\n{content_clean}\n</div>'
    
    st.markdown(full_html, unsafe_allow_html=True)


def sunken_card(
    content: str,
    title: str | None = None,
    animation_index: int = 0,
) -> None:
    """Render an inverted 3D carved surface (sunken panel)."""
    anim_class = f"animate-in animate-in-{animation_index}" if animation_index else "animate-in"
    title_html = f'<h3 style="margin:0 0 0.75rem 0;font-size:1.1rem;font-weight:600;color:var(--text-primary);">{title}</h3>' if title else ""
    
    content_clean = textwrap.dedent(content).strip()
    full_html = f'<div class="medical-input-sunken {anim_class}">\n{title_html}\n{content_clean}\n</div>'
    
    st.markdown(full_html, unsafe_allow_html=True)

# Aliases for backward compatibility during refactor
neu_card = sunken_card
modern_card = raised_card
glass_card = raised_card  # Replace glass with solid 3D per user request


def info_card(
    icon: str,
    title: str,
    value: str,
    color: str = "var(--accent-medical)",
    animation_index: int = 0,
) -> None:
    """Render a compact information card with an icon and single value.

    Args:
        icon: Emoji or icon string.
        title: Card label/title.
        value: Main display value.
        color: Accent color (unused in new design but kept for signature).
        animation_index: Staggered animation delay index.
    """
    anim_class = f"animate-in animate-in-{animation_index}" if animation_index else "animate-in"
    st.markdown(
        f"""
        <div class="metric-card {anim_class}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{title}</div>
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

