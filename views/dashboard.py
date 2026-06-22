"""
HealthAI Pro — Dashboard Page

Welcome screen with quick stats, recent activity, and action cards.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import streamlit as st
import plotly.graph_objects as go

from components.header import page_header
from components.cards import glass_card, neu_card, info_card
from components.metrics import metric_row, severity_distribution_chart
from config.settings import Colors, DISCLAIMER
from services.report_store import ReportStore


def render_dashboard() -> None:
    """Render the Dashboard page."""

    page_header(
        title="Dashboard",
        subtitle="Welcome back — here's your health overview at a glance.",
        icon="",
    )

    store = ReportStore()
    reports = store.list_reports()
    total = len(reports)

    # ── Metrics Row ───────────────────────────────────────────────
    last_date = "Never"
    avg_score = "—"
    severity_counts: dict[str, int] = {"Low": 0, "Moderate": 0, "High": 0, "Critical": 0}

    if reports:
        last_date = reports[0].get("created_at_display", "Unknown")[:12]
        scores = [r.get("analysis", {}).get("health_score", 0) for r in reports]
        avg_score = f"{sum(scores) // len(scores)}"
        for r in reports:
            sev = r.get("analysis", {}).get("overall_severity", "Moderate")
            if sev in severity_counts:
                severity_counts[sev] += 1

    metric_row([
        {"icon": "", "value": str(total), "label": "Total Assessments", "accent": "primary"},
        {"icon": "", "value": last_date, "label": "Last Assessment", "accent": "accent"},
        {"icon": "", "value": avg_score, "label": "Avg Health Score", "accent": "success"},
        {"icon": "", "value": str(severity_counts.get("High", 0) + severity_counts.get("Critical", 0)),
         "label": "High Severity", "accent": "danger"},
    ])

    st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

    # ── Two-column layout ─────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Quick actions
        glass_card(
            title="Quick Actions",
            content="""
            <p style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:1rem;">
                Start a new health assessment or review your previous reports.
            </p>
            """,
            animation_index=1,
        )

        qa_col1, qa_col2 = st.columns(2)
        with qa_col1:
            if st.button("Start New Assessment", use_container_width=True, key="dash_new_assessment", type="primary"):
                st.session_state["current_page"] = "assessment"
                st.rerun()
        with qa_col2:
            if st.button("View Reports", use_container_width=True, key="dash_view_reports"):
                st.session_state["current_page"] = "reports"
                st.rerun()

        st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

        # Recent Activity
        if reports:
            glass_card(
                title="Recent Activity",
                content=_build_recent_activity_html(reports[:5]),
                animation_index=2,
            )
        else:
            glass_card(
                title="Recent Activity",
                content="""
                <div style="text-align:center;padding:2rem 0;">
                    <div style="font-size:3rem;margin-bottom:0.8rem;color:var(--text-muted);">•</div>
                    <p style="color:var(--text-muted);font-size:0.95rem;">No assessments yet.<br>
                    Start your first health assessment to see results here.</p>
                </div>
                """,
                animation_index=2,
            )

    with col_right:
        # Severity Distribution
        if total > 0:
            neu_card(
                title="Severity Distribution",
                content="<div id='sev-chart-placeholder'></div>",
                animation_index=1,
            )
            fig = severity_distribution_chart(severity_counts)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Health tips
        glass_card(
            title="Health Tip",
            content="""
            <p style="color:var(--text-secondary);font-size:0.88rem;line-height:1.6;">
                Regular health check-ups help catch potential issues early.
                Even if you feel fine, periodic assessments create a valuable
                health baseline for future reference.
            </p>
            """,
            animation_index=3,
        )

    # ── Disclaimer ────────────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="disclaimer-banner">{DISCLAIMER}</div>', unsafe_allow_html=True)


def _build_recent_activity_html(reports: list[dict[str, Any]]) -> str:
    """Build HTML for the recent activity feed."""
    items = []
    for r in reports:
        date = r.get("created_at_display", "Unknown date")
        severity = r.get("analysis", {}).get("overall_severity", "Moderate")
        summary = r.get("analysis", {}).get("summary", "No summary available.")
        # Truncate summary
        if len(summary) > 120:
            summary = summary[:117] + "..."

        sev_colors = {"Low": "#22C55E", "Moderate": "#F59E0B", "High": "#EF4444", "Critical": "#7F1D1D"}
        sev_icons = {"Low": "🟢", "Moderate": "🟡", "High": "🔴", "Critical": "🚨"}
        color = sev_colors.get(severity, "#F59E0B")
        icon = sev_icons.get(severity, "🟡")

        items.append(f"""
        <div style="padding:0.8rem 0;border-bottom:1px solid rgba(22,163,74,0.1);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                <span style="font-size:0.82rem;color:var(--text-muted);">{date}</span>
                <span style="font-size:0.75rem;font-weight:600;color:{color};
                    background:rgba({_hex_to_rgb(color)},0.1);padding:0.15rem 0.6rem;
                    border-radius:999px;">{icon} {severity}</span>
            </div>
            <p style="margin:0;font-size:0.85rem;color:#475569;line-height:1.4;">{summary}</p>
        </div>
        """)

    return "".join(items)


def _hex_to_rgb(hex_color: str) -> str:
    """Convert hex color to r,g,b string for rgba()."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r},{g},{b}"
