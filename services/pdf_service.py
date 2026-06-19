"""
HealthAI Pro — PDF Report Service

Generates professional medical-style PDF reports using ReportLab.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config.settings import APP_NAME, DISCLAIMER, REPORTS_DIR, SEVERITY_LEVELS


# ─── Color Palette (ReportLab) ────────────────────────────────────────────────

_PRIMARY = colors.HexColor("#0EA5E9")
_PRIMARY_DARK = colors.HexColor("#0284C7")
_ACCENT = colors.HexColor("#8B5CF6")
_SUCCESS = colors.HexColor("#22C55E")
_WARNING = colors.HexColor("#F59E0B")
_DANGER = colors.HexColor("#EF4444")
_BG_LIGHT = colors.HexColor("#F8FAFC")
_BORDER = colors.HexColor("#E2E8F0")
_TEXT = colors.HexColor("#0F172A")
_TEXT_SECONDARY = colors.HexColor("#475569")
_TEXT_MUTED = colors.HexColor("#94A3B8")

_SEVERITY_COLORS = {
    "Low": _SUCCESS,
    "Moderate": _WARNING,
    "High": _DANGER,
    "Critical": colors.HexColor("#7F1D1D"),
}


class PDFService:
    """Generates professional health assessment PDF reports."""

    @staticmethod
    def generate_report(
        patient_data: dict[str, Any],
        analysis: dict[str, Any],
        output_path: str | Path | None = None,
    ) -> str:
        """Generate a PDF report and return the file path.

        Args:
            patient_data: Patient information dict.
            analysis: Gemini analysis result dict.
            output_path: Optional output path. Defaults to reports/<timestamp>.pdf.

        Returns:
            Absolute path to the generated PDF file.
        """
        if output_path is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = REPORTS_DIR / f"report_{ts}.pdf"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            topMargin=2.0 * cm,
            bottomMargin=2.0 * cm,
            leftMargin=2.0 * cm,
            rightMargin=2.0 * cm,
            title=f"{APP_NAME} — Health Assessment Report",
            author=APP_NAME,
        )

        styles = _build_styles()
        story: list[Any] = []

        # ── Header ────────────────────────────────────────────────
        story.append(Paragraph(f"🏥 {APP_NAME}", styles["title"]))
        story.append(Paragraph("AI-Powered Health Assessment Report", styles["subtitle"]))
        story.append(Spacer(1, 6 * mm))

        # Date line
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"Generated: {date_str}", styles["meta"]))
        story.append(Spacer(1, 4 * mm))
        story.append(_separator())
        story.append(Spacer(1, 4 * mm))

        # ── Patient Information ───────────────────────────────────
        story.append(Paragraph("Patient Information", styles["section_heading"]))
        story.append(Spacer(1, 3 * mm))

        height_cm = patient_data.get("height_cm", "N/A")
        weight_kg = patient_data.get("weight_kg", "N/A")
        bmi_str = "N/A"
        if isinstance(height_cm, (int, float)) and isinstance(weight_kg, (int, float)) and height_cm > 0:
            bmi_str = f"{weight_kg / ((height_cm / 100) ** 2):.1f}"

        patient_rows = [
            ["Age", str(patient_data.get("age", "N/A")), "Gender", str(patient_data.get("gender", "N/A"))],
            ["Height", f"{height_cm} cm", "Weight", f"{weight_kg} kg"],
            ["BMI", bmi_str, "Pain Level", f"{patient_data.get('pain_level', 'N/A')}/10"],
        ]
        story.append(_info_table(patient_rows, styles))
        story.append(Spacer(1, 3 * mm))

        symptoms_list = patient_data.get("symptoms", [])
        if symptoms_list:
            story.append(Paragraph(f"<b>Symptoms:</b> {', '.join(symptoms_list)}", styles["body"]))
        duration = patient_data.get("duration", "")
        if duration:
            story.append(Paragraph(f"<b>Duration:</b> {duration}", styles["body"]))
        conditions = patient_data.get("existing_conditions", [])
        if conditions:
            story.append(Paragraph(f"<b>Existing Conditions:</b> {', '.join(conditions)}", styles["body"]))
        meds = patient_data.get("medications", "")
        if meds:
            story.append(Paragraph(f"<b>Medications:</b> {meds}", styles["body"]))

        story.append(Spacer(1, 4 * mm))
        story.append(_separator())
        story.append(Spacer(1, 4 * mm))

        # ── Overall Assessment ────────────────────────────────────
        story.append(Paragraph("Overall Assessment", styles["section_heading"]))
        story.append(Spacer(1, 3 * mm))

        severity = analysis.get("overall_severity", "Moderate")
        score = analysis.get("health_score", 50)
        sev_color = _SEVERITY_COLORS.get(severity, _WARNING)

        summary_text = analysis.get("summary", "No summary available.")
        story.append(Paragraph(summary_text, styles["body"]))
        story.append(Spacer(1, 2 * mm))

        assessment_rows = [
            ["Severity Level", severity, "Health Score", f"{score}/100"],
        ]
        story.append(_assessment_table(assessment_rows, sev_color, styles))
        story.append(Spacer(1, 4 * mm))

        # ── General Information ───────────────────────────────────
        gen_info = analysis.get("general_information", "")
        if gen_info:
            story.append(Paragraph("General Information", styles["section_heading"]))
            story.append(Spacer(1, 2 * mm))
            story.append(Paragraph(gen_info, styles["body"]))
            story.append(Spacer(1, 4 * mm))

        # ── Possible Conditions ───────────────────────────────────
        conditions_list = analysis.get("possible_conditions", [])
        if conditions_list:
            story.append(Paragraph("Possible Conditions", styles["section_heading"]))
            story.append(Spacer(1, 2 * mm))
            for cond in conditions_list:
                name = cond.get("name", "Unknown")
                likelihood = cond.get("likelihood", "")
                desc = cond.get("description", "")
                story.append(Paragraph(f"• <b>{name}</b> (Likelihood: {likelihood})", styles["body"]))
                if desc:
                    story.append(Paragraph(f"  {desc}", styles["body_small"]))
            story.append(Spacer(1, 4 * mm))

        # ── Treatments ────────────────────────────────────────────
        treatments = analysis.get("commonly_used_treatments", [])
        if treatments:
            story.append(Paragraph("Commonly Used Treatments", styles["section_heading"]))
            story.append(Spacer(1, 2 * mm))
            for t in treatments:
                name = t.get("name", "")
                ttype = t.get("type", "")
                desc = t.get("description", "")
                story.append(Paragraph(f"• <b>{name}</b> ({ttype})", styles["body"]))
                if desc:
                    story.append(Paragraph(f"  {desc}", styles["body_small"]))
                pros = t.get("pros", [])
                cons = t.get("cons", [])
                if pros:
                    story.append(Paragraph(f"  ✅ Pros: {', '.join(pros)}", styles["body_small"]))
                if cons:
                    story.append(Paragraph(f"  ⚠️ Cons: {', '.join(cons)}", styles["body_small"]))
                story.append(Spacer(1, 1.5 * mm))
            story.append(Spacer(1, 3 * mm))

        # ── Warning Signs ─────────────────────────────────────────
        warnings = analysis.get("warning_signs", [])
        if warnings:
            story.append(Paragraph("⚠ Warning Signs", styles["section_heading_danger"]))
            story.append(Spacer(1, 2 * mm))
            for w in warnings:
                story.append(Paragraph(f"• {w}", styles["body"]))
            story.append(Spacer(1, 4 * mm))

        # ── When to See a Doctor ──────────────────────────────────
        doctor_triggers = analysis.get("when_to_see_doctor", [])
        if doctor_triggers:
            story.append(Paragraph("When to Consult a Doctor", styles["section_heading"]))
            story.append(Spacer(1, 2 * mm))
            for d in doctor_triggers:
                story.append(Paragraph(f"• {d}", styles["body"]))
            story.append(Spacer(1, 4 * mm))

        # ── Lifestyle Recommendations ─────────────────────────────
        lifestyle = analysis.get("lifestyle_recommendations", [])
        if lifestyle:
            story.append(Paragraph("Lifestyle Recommendations", styles["section_heading"]))
            story.append(Spacer(1, 2 * mm))
            for l in lifestyle:
                story.append(Paragraph(f"• {l}", styles["body"]))
            story.append(Spacer(1, 4 * mm))

        # ── Disclaimer ────────────────────────────────────────────
        story.append(_separator())
        story.append(Spacer(1, 3 * mm))
        disclaimer_clean = DISCLAIMER.replace("**", "").replace("⚕️ ", "")
        story.append(Paragraph(f"<i>{disclaimer_clean}</i>", styles["disclaimer"]))

        # ── Build PDF ─────────────────────────────────────────────
        doc.build(story)
        return str(output_path.resolve())


# ─── Private helpers ──────────────────────────────────────────────────────────

def _build_styles() -> dict[str, ParagraphStyle]:
    """Build the custom paragraph styles for the PDF."""
    base = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "CustomTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=_PRIMARY_DARK,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "subtitle": ParagraphStyle(
            "CustomSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            textColor=_TEXT_SECONDARY,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=_TEXT_MUTED,
        ),
        "section_heading": ParagraphStyle(
            "SectionHeading",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=_PRIMARY_DARK,
            spaceBefore=4,
            spaceAfter=2,
        ),
        "section_heading_danger": ParagraphStyle(
            "SectionHeadingDanger",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=_DANGER,
            spaceBefore=4,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "CustomBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=_TEXT,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=3,
        ),
        "body_small": ParagraphStyle(
            "BodySmall",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=_TEXT_SECONDARY,
            leading=13,
            leftIndent=12,
            spaceAfter=2,
        ),
        "disclaimer": ParagraphStyle(
            "Disclaimer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=_TEXT_MUTED,
            leading=11,
            alignment=TA_CENTER,
        ),
    }


def _separator() -> Table:
    """Return a thin horizontal line as a table."""
    t = Table([[""]],  colWidths=["100%"])
    t.setStyle(
        TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 0.5, _BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ])
    )
    return t


def _info_table(rows: list[list[str]], styles: dict) -> Table:
    """Build a styled key–value info table."""
    data = []
    for row in rows:
        styled_row = []
        for i, cell in enumerate(row):
            if i % 2 == 0:
                styled_row.append(Paragraph(f"<b>{cell}</b>", styles["body_small"]))
            else:
                styled_row.append(Paragraph(cell, styles["body"]))
        data.append(styled_row)

    t = Table(data, colWidths=["18%", "32%", "18%", "32%"])
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), _BG_LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.5, _BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, _BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ])
    )
    return t


def _assessment_table(rows: list[list[str]], sev_color: colors.HexColor, styles: dict) -> Table:
    """Build the severity / score summary table."""
    data = []
    for row in rows:
        data.append([
            Paragraph(f"<b>{row[0]}</b>", styles["body"]),
            Paragraph(f"<b>{row[1]}</b>", styles["body"]),
            Paragraph(f"<b>{row[2]}</b>", styles["body"]),
            Paragraph(f"<b>{row[3]}</b>", styles["body"]),
        ])

    t = Table(data, colWidths=["22%", "28%", "22%", "28%"])
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), _BG_LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.5, _BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, _BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("TEXTCOLOR", (1, 0), (1, 0), sev_color),
        ])
    )
    return t
