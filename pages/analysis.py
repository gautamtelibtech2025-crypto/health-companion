"""
HealthAI Pro — AI Analysis Page

Displays the Gemini analysis results in rich, styled sections.
"""

from __future__ import annotations

import time
from typing import Any

import streamlit as st

from components.header import page_header
from components.cards import glass_card, neu_card, status_badge
from components.metrics import health_score_gauge, metric_row
from config.settings import Colors, DISCLAIMER, SEVERITY_LEVELS
from services.gemini_service import GeminiService
from services.pdf_service import PDFService
from services.report_store import ReportStore


def render_analysis() -> None:
    """Render the AI Analysis page."""

    page_header(
        title="AI Analysis",
        subtitle="Review your AI-powered health assessment results.",
        icon="🧠",
    )

    # ── Check if we should run a new analysis ─────────────────────
    if st.session_state.get("run_analysis"):
        st.session_state["run_analysis"] = False
        _run_analysis()
        return

    # ── Display existing results ──────────────────────────────────
    analysis = st.session_state.get("last_analysis")
    patient_data = st.session_state.get("assessment_data", {})

    if not analysis:
        glass_card(
            title="No Analysis Available",
            content="""
            <div style="text-align:center;padding:2rem 0;">
                <div style="font-size:3rem;margin-bottom:0.8rem;">🧠</div>
                <p style="color:#94A3B8;font-size:0.95rem;">
                    Complete a health assessment first to see AI analysis results here.
                </p>
            </div>
            """,
            animation_index=1,
        )

        if st.button("🩺  Start Assessment", key="analysis_start"):
            st.session_state["current_page"] = "assessment"
            st.rerun()
        return

    # ── Results display ───────────────────────────────────────────
    severity = analysis.get("overall_severity", "Moderate")
    score = analysis.get("health_score", 50)
    summary = analysis.get("summary", "")
    sev_data = SEVERITY_LEVELS.get(severity, SEVERITY_LEVELS["Moderate"])

    # Top metrics
    metric_row([
        {"icon": sev_data["icon"], "value": severity, "label": "Severity Level",
         "accent": "danger" if severity in ("High", "Critical") else ("warning" if severity == "Moderate" else "success")},
        {"icon": "💯", "value": str(score), "label": "Health Score", "accent": "primary"},
    ])

    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

    # Gauge + Summary side by side
    col1, col2 = st.columns([2, 3])

    with col1:
        fig = health_score_gauge(score)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        badge_html = status_badge(severity, severity)
        glass_card(
            title="Summary",
            content=f"""
            <div style="margin-bottom:0.6rem;">{badge_html}</div>
            <p style="color:#475569;font-size:0.9rem;line-height:1.6;">{summary}</p>
            """,
            animation_index=1,
        )

    # ── General Information ───────────────────────────────────────
    gen_info = analysis.get("general_information", "")
    if gen_info:
        glass_card(
            title="📖 General Information",
            content=f'<p style="color:#475569;font-size:0.9rem;line-height:1.7;">{gen_info}</p>',
            animation_index=2,
        )

    # ── Possible Conditions ───────────────────────────────────────
    conditions = analysis.get("possible_conditions", [])
    if conditions:
        st.markdown("### 🔍 Possible Conditions")
        for i, cond in enumerate(conditions):
            name = cond.get("name", "Unknown")
            likelihood = cond.get("likelihood", "Unknown")
            desc = cond.get("description", "")

            lk_colors = {"Low": "#22C55E", "Moderate": "#F59E0B", "High": "#EF4444"}
            lk_color = lk_colors.get(likelihood, "#94A3B8")

            st.markdown(
                f"""
                <div class="neu-card animate-in animate-in-{min(i+1, 4)}">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                        <h4 style="margin:0;font-size:1rem;color:#0F172A;">{name}</h4>
                        <span style="font-size:0.75rem;font-weight:600;color:{lk_color};
                            background:rgba({_hex_to_rgb(lk_color)},0.1);padding:0.15rem 0.6rem;
                            border-radius:999px;">Likelihood: {likelihood}</span>
                    </div>
                    <p style="margin:0;font-size:0.88rem;color:#475569;line-height:1.5;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Treatments ────────────────────────────────────────────────
    treatments = analysis.get("commonly_used_treatments", [])
    if treatments:
        st.markdown("### 💊 Commonly Used Treatments")
        for t in treatments:
            name = t.get("name", "")
            ttype = t.get("type", "")
            desc = t.get("description", "")
            pros = t.get("pros", [])
            cons = t.get("cons", [])

            with st.expander(f"💊 {name}  —  {ttype}", expanded=False):
                if desc:
                    st.markdown(f"**Description:** {desc}")
                col_p, col_c = st.columns(2)
                with col_p:
                    st.markdown("**✅ Pros**")
                    for p in pros:
                        st.markdown(f"- {p}")
                with col_c:
                    st.markdown("**⚠️ Cons**")
                    for c in cons:
                        st.markdown(f"- {c}")

    # ── Warning Signs ─────────────────────────────────────────────
    warnings = analysis.get("warning_signs", [])
    if warnings:
        warning_items = "".join(f'<li style="margin-bottom:0.3rem;">{w}</li>' for w in warnings)
        st.markdown(
            f"""
            <div class="glass-card animate-in" style="border-left:4px solid #EF4444;background:rgba(239,68,68,0.04);">
                <h4 style="margin:0 0 0.5rem 0;color:#EF4444;">⚠️ Warning Signs</h4>
                <ul style="margin:0;padding-left:1.2rem;color:#475569;font-size:0.9rem;line-height:1.7;">
                    {warning_items}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── When to See a Doctor ──────────────────────────────────────
    doctor_items = analysis.get("when_to_see_doctor", [])
    if doctor_items:
        doc_html = "".join(f'<li style="margin-bottom:0.3rem;">{d}</li>' for d in doctor_items)
        st.markdown(
            f"""
            <div class="glass-card animate-in" style="border-left:4px solid #3B82F6;background:rgba(59,130,246,0.04);">
                <h4 style="margin:0 0 0.5rem 0;color:#3B82F6;">🩺 When to Consult a Doctor</h4>
                <ul style="margin:0;padding-left:1.2rem;color:#475569;font-size:0.9rem;line-height:1.7;">
                    {doc_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Lifestyle Recommendations ─────────────────────────────────
    lifestyle = analysis.get("lifestyle_recommendations", [])
    if lifestyle:
        life_html = "".join(f'<li style="margin-bottom:0.3rem;">{l}</li>' for l in lifestyle)
        glass_card(
            title="🌿 Lifestyle Recommendations",
            content=f'<ul style="margin:0;padding-left:1.2rem;color:#475569;font-size:0.9rem;line-height:1.7;">{life_html}</ul>',
            animation_index=3,
        )

    # ── Recommended Actions ───────────────────────────────────────
    actions = analysis.get("recommended_actions", [])
    if actions:
        actions_html = "".join(f'<li style="margin-bottom:0.3rem;">{a}</li>' for a in actions)
        glass_card(
            title="✅ Recommended Actions",
            content=f'<ul style="margin:0;padding-left:1.2rem;color:#475569;font-size:0.9rem;line-height:1.7;">{actions_html}</ul>',
            animation_index=4,
        )

    # ── Action buttons ────────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        if st.button("📄  Generate PDF Report", key="gen_pdf", use_container_width=True):
            _generate_and_save_pdf(patient_data, analysis)

    with btn_col2:
        if st.button("🩺  New Assessment", key="new_assessment_btn", use_container_width=True):
            st.session_state["wizard_step"] = 1
            st.session_state["assessment_data"] = {}
            st.session_state["last_analysis"] = None
            st.session_state["current_page"] = "assessment"
            st.rerun()

    with btn_col3:
        if st.button("📊  Go to Dashboard", key="go_dashboard_btn", use_container_width=True):
            st.session_state["current_page"] = "dashboard"
            st.rerun()

    # ── Disclaimer ────────────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="disclaimer-banner">{DISCLAIMER}</div>', unsafe_allow_html=True)


# ─── Private Helpers ──────────────────────────────────────────────────────────

def _run_analysis() -> None:
    """Execute the Gemini analysis with a loading animation."""
    patient_data = st.session_state.get("assessment_data", {})

    if not patient_data:
        st.error("No assessment data found. Please complete the assessment first.")
        return

    if not GeminiService.is_configured():
        st.error("⚠️ Gemini API key not configured. Please go to **Settings** and add your API key.")
        if st.button("⚙️  Go to Settings"):
            st.session_state["current_page"] = "settings"
            st.rerun()
        return

    # Loading animation
    with st.spinner(""):
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;padding:3rem;">
                <div style="font-size:3rem;margin-bottom:1rem;" class="pulse-glow">🧠</div>
                <h3 style="margin:0 0 0.5rem 0;color:#0F172A;">Analyzing Your Health Data</h3>
                <p style="color:#94A3B8;font-size:0.9rem;">
                    Our AI is reviewing your symptoms and medical history...<br>
                    This usually takes 10–20 seconds.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            analysis = GeminiService.analyze_health(patient_data)
            st.session_state["last_analysis"] = analysis
            st.rerun()
        except RuntimeError as e:
            st.error(f"Analysis failed: {e}")


def _generate_and_save_pdf(patient_data: dict, analysis: dict) -> None:
    """Generate a PDF and save the report."""
    try:
        with st.spinner("Generating PDF report..."):
            pdf_path = PDFService.generate_report(patient_data, analysis)

            store = ReportStore()
            report_id = store.save_report(patient_data, analysis, pdf_path)

        st.success(f"✅ Report saved! ID: `{report_id}`")

        # Offer download
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️  Download PDF",
                data=f.read(),
                file_name=f"HealthAI_Report_{report_id}.pdf",
                mime="application/pdf",
                key="download_pdf_btn",
            )
    except Exception as e:
        st.error(f"Failed to generate PDF: {e}")


def _hex_to_rgb(hex_color: str) -> str:
    """Convert hex color to r,g,b string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r},{g},{b}"
