"""
HealthAI Pro — Health Assessment Page

Multi-step wizard for collecting patient health information.
"""

from __future__ import annotations

import streamlit as st

from components.header import page_header
from components.cards import glass_card
from components.forms import (
    styled_number_input,
    styled_selectbox,
    styled_multiselect,
    styled_slider,
    styled_text_area,
    wizard_progress,
)
from config.settings import (
    COMMON_SYMPTOMS,
    DISCLAIMER,
    DURATION_OPTIONS,
    EXISTING_CONDITIONS,
    GENDER_OPTIONS,
)


_WIZARD_STEPS = ["Personal Info", "Symptoms", "Duration & Severity", "Medical History", "Review"]


def render_assessment() -> None:
    """Render the Health Assessment wizard page."""

    page_header(
        title="Health Assessment",
        subtitle="Answer a few questions so our AI can provide personalized insights.",
        icon="🩺",
    )

    # Disclaimer
    st.markdown(f'<div class="disclaimer-banner">{DISCLAIMER}</div>', unsafe_allow_html=True)

    # ── Initialize wizard state ───────────────────────────────────
    if "wizard_step" not in st.session_state:
        st.session_state["wizard_step"] = 1

    if "assessment_data" not in st.session_state:
        st.session_state["assessment_data"] = {}

    step = st.session_state["wizard_step"]
    data: dict = st.session_state["assessment_data"]

    # ── Progress indicator ────────────────────────────────────────
    wizard_progress(step, _WIZARD_STEPS)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # ── Step content ──────────────────────────────────────────────
    if step == 1:
        _step_personal_info(data)
    elif step == 2:
        _step_symptoms(data)
    elif step == 3:
        _step_duration(data)
    elif step == 4:
        _step_medical_history(data)
    elif step == 5:
        _step_review(data)

    # ── Navigation buttons ────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    nav_cols = st.columns([1, 1, 1])

    with nav_cols[0]:
        if step > 1:
            if st.button("← Previous", key="wiz_prev", use_container_width=True):
                st.session_state["wizard_step"] = step - 1
                st.rerun()

    with nav_cols[2]:
        if step < 5:
            if st.button("Next →", key="wiz_next", use_container_width=True):
                # Basic validation
                valid, msg = _validate_step(step, data)
                if valid:
                    st.session_state["wizard_step"] = step + 1
                    st.rerun()
                else:
                    st.error(msg)
        elif step == 5:
            if st.button("🧠 Analyze with AI", key="wiz_submit", use_container_width=True):
                st.session_state["current_page"] = "analysis"
                st.session_state["run_analysis"] = True
                st.rerun()


# ─── Step Renderers ───────────────────────────────────────────────────────────

def _step_personal_info(data: dict) -> None:
    """Step 1: Personal information."""
    glass_card(
        title="👤 Personal Information",
        content="<p style='color:var(--text-secondary);font-size:0.88rem;'>Tell us about yourself.</p>",
        animation_index=1,
    )

    col1, col2 = st.columns(2)
    with col1:
        data["age"] = styled_number_input(
            "Age",
            key="age",
            min_value=1,
            max_value=120,
            value=data.get("age", 30),
            step=1,
            help="Your current age in years.",
        )
    with col2:
        data["gender"] = styled_selectbox(
            "Gender",
            GENDER_OPTIONS,
            key="gender",
            index=GENDER_OPTIONS.index(data["gender"]) if data.get("gender") in GENDER_OPTIONS else 0,
        )

    col3, col4 = st.columns(2)
    with col3:
        data["height_cm"] = styled_number_input(
            "Height (cm)",
            key="height_cm",
            min_value=50,
            max_value=250,
            value=data.get("height_cm", 170),
            step=1,
        )
    with col4:
        data["weight_kg"] = styled_number_input(
            "Weight (kg)",
            key="weight_kg",
            min_value=10,
            max_value=300,
            value=data.get("weight_kg", 70),
            step=1,
        )

    # BMI calculation
    h = data.get("height_cm", 0)
    w = data.get("weight_kg", 0)
    if h > 0 and w > 0:
        bmi = w / ((h / 100) ** 2)
        category, color = _bmi_category(bmi)
        st.markdown(
            f"""
            <div class="medical-input-sunken animate-in animate-in-2" style="text-align:center;padding:1rem;">
                <span style="font-size:0.82rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">
                    Body Mass Index
                </span>
                <div style="font-size:2rem;font-weight:800;color:{color};margin:0.3rem 0;">
                    {bmi:.1f}
                </div>
                <span style="font-size:0.85rem;color:{color};font-weight:600;">{category}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _step_symptoms(data: dict) -> None:
    """Step 2: Symptom selection."""
    glass_card(
        title="🤒 Symptoms",
        content="<p style='color:var(--text-secondary);font-size:0.88rem;'>Select your current symptoms.</p>",
        animation_index=1,
    )

    data["symptoms"] = styled_multiselect(
        "Select Symptoms",
        COMMON_SYMPTOMS,
        key="symptoms",
        default=data.get("symptoms", []),
        help="Choose all symptoms you are currently experiencing.",
    )

    data["other_symptoms"] = styled_text_area(
        "Other Symptoms (not listed above)",
        key="other_symptoms",
        value=data.get("other_symptoms", ""),
        placeholder="Describe any other symptoms you're experiencing...",
        help="Free-text field for symptoms not in the list.",
    )


def _step_duration(data: dict) -> None:
    """Step 3: Duration and severity."""
    glass_card(
        title="⏱️ Duration & Severity",
        content="<p style='color:var(--text-secondary);font-size:0.88rem;'>How long have you had these symptoms and how severe are they?</p>",
        animation_index=1,
    )

    data["duration"] = styled_selectbox(
        "How long have you had these symptoms?",
        DURATION_OPTIONS,
        key="duration",
        index=DURATION_OPTIONS.index(data["duration"]) if data.get("duration") in DURATION_OPTIONS else 0,
    )

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    data["pain_level"] = styled_slider(
        "Pain / Discomfort Level",
        key="pain_level",
        min_value=0,
        max_value=10,
        value=data.get("pain_level", 3),
        step=1,
        help="0 = No pain, 10 = Worst pain imaginable",
    )

    # Visual pain indicator
    level = data["pain_level"]
    if level <= 3:
        pain_label, pain_color, pain_emoji = "Mild", "#22C55E", "😊"
    elif level <= 6:
        pain_label, pain_color, pain_emoji = "Moderate", "#F59E0B", "😐"
    elif level <= 8:
        pain_label, pain_color, pain_emoji = "Severe", "#EF4444", "😣"
    else:
        pain_label, pain_color, pain_emoji = "Very Severe", "#7F1D1D", "😭"

    st.markdown(
        f"""
        <div style="text-align:center;margin:0.5rem 0;">
            <span style="font-size:2.5rem;">{pain_emoji}</span>
            <div style="font-size:0.9rem;font-weight:600;color:{pain_color};margin-top:0.2rem;">
                {pain_label} ({level}/10)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _step_medical_history(data: dict) -> None:
    """Step 4: Medical history."""
    glass_card(
        title="📋 Medical History",
        content="<p style='color:var(--text-secondary);font-size:0.88rem;'>Help us understand your medical background.</p>",
        animation_index=1,
    )

    data["existing_conditions"] = styled_multiselect(
        "Existing Medical Conditions",
        EXISTING_CONDITIONS,
        key="existing_conditions",
        default=data.get("existing_conditions", []),
    )

    data["medications"] = styled_text_area(
        "Current Medications",
        key="medications",
        value=data.get("medications", ""),
        placeholder="List any medications you are currently taking...",
        height=80,
    )

    data["allergies"] = styled_text_area(
        "Known Allergies",
        key="allergies",
        value=data.get("allergies", ""),
        placeholder="List any known allergies...",
        height=80,
    )

    data["additional_notes"] = styled_text_area(
        "Additional Notes",
        key="additional_notes",
        value=data.get("additional_notes", ""),
        placeholder="Anything else you'd like the AI to consider...",
        height=80,
    )


def _step_review(data: dict) -> None:
    """Step 5: Review all collected data before submitting."""
    glass_card(
        title="✅ Review Your Information",
        content="<p style='color:var(--text-secondary);font-size:0.88rem;'>Please review the information below before submitting for AI analysis.</p>",
        animation_index=1,
    )

    # Personal info
    h = data.get("height_cm", 0)
    w = data.get("weight_kg", 0)
    bmi_str = f"{w / ((h / 100) ** 2):.1f}" if h > 0 and w > 0 else "N/A"

    st.markdown(
        f"""
        <div class="medical-input-sunken">
            <h4 style="margin:0 0 0.6rem 0;color:var(--accent);">👤 Personal Info</h4>
            <table style="width:100%;font-size:0.88rem;color:var(--text-secondary);">
                <tr><td style="padding:0.3rem 0;font-weight:600;width:40%;">Age</td>
                    <td>{data.get('age', 'N/A')}</td></tr>
                <tr><td style="padding:0.3rem 0;font-weight:600;">Gender</td>
                    <td>{data.get('gender', 'N/A')}</td></tr>
                <tr><td style="padding:0.3rem 0;font-weight:600;">Height</td>
                    <td>{h} cm</td></tr>
                <tr><td style="padding:0.3rem 0;font-weight:600;">Weight</td>
                    <td>{w} kg</td></tr>
                <tr><td style="padding:0.3rem 0;font-weight:600;">BMI</td>
                    <td>{bmi_str}</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    symptoms = data.get("symptoms", [])
    other = data.get("other_symptoms", "")
    all_symptoms = ", ".join(symptoms) if symptoms else "None selected"
    if other:
        all_symptoms += f" | Other: {other}"

    st.markdown(
        f"""
        <div class="medical-input-sunken">
            <h4 style="margin:0 0 0.6rem 0;color:var(--accent);">🤒 Symptoms</h4>
            <p style="font-size:0.88rem;color:var(--text-secondary);margin:0;">{all_symptoms}</p>
            <p style="font-size:0.88rem;color:var(--text-secondary);margin:0.3rem 0 0 0;">
                <strong>Duration:</strong> {data.get('duration', 'N/A')} &nbsp;|&nbsp;
                <strong>Pain Level:</strong> {data.get('pain_level', 'N/A')}/10
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    conditions = ", ".join(data.get("existing_conditions", [])) or "None"
    meds = data.get("medications", "None") or "None"

    st.markdown(
        f"""
        <div class="medical-input-sunken">
            <h4 style="margin:0 0 0.6rem 0;color:var(--accent);">📋 Medical History</h4>
            <p style="font-size:0.88rem;color:var(--text-secondary);margin:0;">
                <strong>Conditions:</strong> {conditions}<br>
                <strong>Medications:</strong> {meds}<br>
                <strong>Allergies:</strong> {data.get('allergies', 'None') or 'None'}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _validate_step(step: int, data: dict) -> tuple[bool, str]:
    """Validate the current wizard step. Returns (ok, error_message)."""
    if step == 1:
        if not data.get("age") or data["age"] < 1:
            return False, "Please enter a valid age."
        if not data.get("height_cm") or data["height_cm"] < 50:
            return False, "Please enter a valid height."
        if not data.get("weight_kg") or data["weight_kg"] < 10:
            return False, "Please enter a valid weight."
    elif step == 2:
        if not data.get("symptoms") and not data.get("other_symptoms", "").strip():
            return False, "Please select at least one symptom or describe your symptoms."
    return True, ""


def _bmi_category(bmi: float) -> tuple[str, str]:
    """Return (category_name, hex_color) for a BMI value."""
    if bmi < 18.5:
        return "Underweight", "#3B82F6"
    elif bmi < 25:
        return "Normal", "#22C55E"
    elif bmi < 30:
        return "Overweight", "#F59E0B"
    else:
        return "Obese", "#EF4444"
