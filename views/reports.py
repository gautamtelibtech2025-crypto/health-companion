"""
HealthAI Pro — Previous Reports Page

Browse, view, download, and delete saved health assessment reports.
"""

from __future__ import annotations

import os
from typing import Any

import streamlit as st

from components.header import page_header
from components.cards import glass_card, status_badge
from config.settings import SEVERITY_LEVELS
from services.report_store import ReportStore


def render_reports() -> None:
    """Render the Previous Reports page."""

    page_header(
        title="Previous Reports",
        subtitle="Browse and manage your saved health assessment reports.",
        icon="📄",
    )

    store = ReportStore()
    reports = store.list_reports()

    if not reports:
        glass_card(
            title="No Reports Yet",
            content="""
            <div style="text-align:center;padding:2rem 0;">
                <div style="font-size:3rem;margin-bottom:0.8rem;">📄</div>
                <p style="color:#94A3B8;font-size:0.95rem;">
                    You haven't generated any reports yet.<br>
                    Complete a health assessment and generate a PDF to see it here.
                </p>
            </div>
            """,
            animation_index=1,
        )
        if st.button("🩺  Start Assessment", key="reports_start"):
            st.session_state["current_page"] = "assessment"
            st.rerun()
        return

    # ── Search / Filter ───────────────────────────────────────────
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 Search reports", placeholder="Search by condition, symptom, or date...",
                              key="report_search", label_visibility="collapsed")
    with col_filter:
        severity_filter = st.selectbox("Filter by severity", ["All", "Low", "Moderate", "High", "Critical"],
                                       key="severity_filter", label_visibility="collapsed")

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # ── Filter logic ──────────────────────────────────────────────
    filtered = reports
    if severity_filter != "All":
        filtered = [r for r in filtered if r.get("analysis", {}).get("overall_severity") == severity_filter]
    if search.strip():
        q = search.strip().lower()
        filtered = [r for r in filtered if _report_matches_search(r, q)]

    # ── Stats bar ─────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <span style="font-size:0.85rem;color:#94A3B8;">
                Showing {len(filtered)} of {len(reports)} reports
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Report list ───────────────────────────────────────────────
    for idx, report in enumerate(filtered):
        _render_report_card(report, idx, store)


def _render_report_card(report: dict[str, Any], idx: int, store: ReportStore) -> None:
    """Render a single report card with expandable details."""

    report_id = report.get("id", "unknown")
    date = report.get("created_at_display", "Unknown date")
    analysis = report.get("analysis", {})
    patient = report.get("patient_data", {})
    severity = analysis.get("overall_severity", "Moderate")
    score = analysis.get("health_score", 50)
    summary = analysis.get("summary", "No summary available.")
    pdf_path = report.get("pdf_path")

    sev_data = SEVERITY_LEVELS.get(severity, SEVERITY_LEVELS["Moderate"])
    badge = status_badge(severity, severity)

    # Truncate summary for card preview
    short_summary = summary[:150] + "..." if len(summary) > 150 else summary

    # Symptoms preview
    symptoms = patient.get("symptoms", [])
    symptoms_str = ", ".join(symptoms[:4])
    if len(symptoms) > 4:
        symptoms_str += f" +{len(symptoms) - 4} more"

    with st.expander(f"📋  {date}  —  {severity}  —  Score: {score}/100", expanded=False):
        st.markdown(
            f"""
            <div style="margin-bottom:0.8rem;">
                {badge}
                <span style="font-size:0.82rem;color:#94A3B8;margin-left:0.8rem;">
                    Report ID: {report_id}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Patient info row
        age = patient.get("age", "N/A")
        gender = patient.get("gender", "N/A")
        st.markdown(
            f"""
            <div class="neu-card" style="padding:1rem;">
                <div style="display:flex;gap:2rem;font-size:0.88rem;color:#475569;">
                    <span><strong>Age:</strong> {age}</span>
                    <span><strong>Gender:</strong> {gender}</span>
                    <span><strong>Score:</strong> {score}/100</span>
                </div>
                {f'<div style="margin-top:0.4rem;font-size:0.85rem;color:#475569;"><strong>Symptoms:</strong> {symptoms_str}</div>' if symptoms_str else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Summary
        st.markdown(f"**Summary:** {summary}")

        # Conditions
        conditions = analysis.get("possible_conditions", [])
        if conditions:
            st.markdown("**Possible Conditions:**")
            for c in conditions:
                st.markdown(f"- {c.get('name', 'Unknown')} (Likelihood: {c.get('likelihood', 'N/A')})")

        # Warning signs
        warnings = analysis.get("warning_signs", [])
        if warnings:
            st.markdown("**⚠️ Warning Signs:**")
            for w in warnings:
                st.markdown(f"- {w}")

        # Action buttons
        btn_col1, btn_col2, btn_col3 = st.columns(3)

        with btn_col1:
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download PDF",
                        data=f.read(),
                        file_name=f"HealthAI_{report_id}.pdf",
                        mime="application/pdf",
                        key=f"dl_{report_id}",
                        use_container_width=True,
                    )
            else:
                st.button("📄 PDF not available", key=f"no_pdf_{report_id}", disabled=True,
                         use_container_width=True)

        with btn_col2:
            if st.button("🧠 View Full Analysis", key=f"view_{report_id}", use_container_width=True):
                st.session_state["last_analysis"] = analysis
                st.session_state["assessment_data"] = patient
                st.session_state["current_page"] = "analysis"
                st.rerun()

        with btn_col3:
            if st.button("🗑️ Delete", key=f"del_{report_id}", use_container_width=True):
                store.delete_report(report_id)
                st.success(f"Report {report_id} deleted.")
                st.rerun()


def _report_matches_search(report: dict[str, Any], query: str) -> bool:
    """Check if a report matches the search query."""
    searchable = " ".join([
        report.get("created_at_display", ""),
        " ".join(report.get("patient_data", {}).get("symptoms", [])),
        report.get("analysis", {}).get("summary", ""),
        " ".join(c.get("name", "") for c in report.get("analysis", {}).get("possible_conditions", [])),
        report.get("analysis", {}).get("overall_severity", ""),
    ]).lower()
    return query in searchable
