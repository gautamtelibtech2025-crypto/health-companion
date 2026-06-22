"""
HealthAI Pro — Gemini AI Service

Handles all interaction with the Google Gemini API for health analysis.
"""

from __future__ import annotations

import json
import re
from typing import Any

import google.generativeai as genai

from config.settings import GEMINI_MODEL


class GeminiService:
    """Wrapper around the Google Generative AI SDK for health analysis."""

    _configured: bool = False

    @classmethod
    def configure(cls, api_key: str) -> None:
        """Configure the Gemini SDK with the given API key.

        Args:
            api_key: Google Gemini API key.
        """
        genai.configure(api_key=api_key)
        cls._configured = True

    @classmethod
    def is_configured(cls) -> bool:
        """Return True if the API key has been set."""
        return cls._configured

    @classmethod
    def get_model_name(cls) -> str:
        """Get the active model name from session state or settings."""
        try:
            import streamlit as st
            if "selected_model" in st.session_state:
                return st.session_state["selected_model"]
        except Exception:
            pass
        return GEMINI_MODEL

    @classmethod
    def test_connection(cls) -> tuple[bool, str]:
        """Test the Gemini API connection.

        Returns:
            (success, message) tuple.
        """
        if not cls._configured:
            return False, "API key not configured."
        model_name = cls.get_model_name()
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'connection successful' in exactly two words.")
            return True, f"✅ Connection successful. Model: {model_name}"
        except Exception as exc:
            return False, f"❌ Connection failed: {exc}"

    @classmethod
    def analyze_health(cls, patient_data: dict[str, Any]) -> dict[str, Any]:
        """Send patient data to Gemini and return a structured health analysis.

        Args:
            patient_data: Dict with keys like 'age', 'gender', 'symptoms', etc.

        Returns:
            Parsed JSON dict with analysis results.

        Raises:
            RuntimeError: If API is not configured or call fails.
        """
        if not cls._configured:
            raise RuntimeError("Gemini API key not configured. Go to Settings to add your key.")

        prompt = _build_analysis_prompt(patient_data)
        model_name = cls.get_model_name()

        try:
            model = genai.GenerativeModel(
                model_name,
                generation_config={
                    "temperature": 0.4,
                    "top_p": 0.95,
                    "max_output_tokens": 4096,
                },
            )
            response = model.generate_content(prompt)
            return _parse_response(response.text)
        except Exception as exc:
            raise RuntimeError(f"Gemini API error: {exc}") from exc


# ─── Private helpers ──────────────────────────────────────────────────────────

def _build_analysis_prompt(data: dict[str, Any]) -> str:
    """Build the structured prompt for the Gemini model."""

    symptoms = ", ".join(data.get("symptoms", [])) or "Not specified"
    conditions = ", ".join(data.get("existing_conditions", [])) or "None"
    medications = data.get("medications", "None")
    additional = data.get("additional_notes", "None")

    # Calculate BMI if height & weight provided
    height_cm = data.get("height_cm", 0)
    weight_kg = data.get("weight_kg", 0)
    bmi_str = ""
    if height_cm > 0 and weight_kg > 0:
        bmi = weight_kg / ((height_cm / 100) ** 2)
        bmi_str = f"BMI: {bmi:.1f}"

    return f"""You are a knowledgeable medical information assistant. Analyze the following patient information and provide a detailed health assessment.

IMPORTANT: You are NOT diagnosing. You are providing general health information and suggestions. Always recommend consulting a real doctor.

PATIENT INFORMATION:
- Age: {data.get('age', 'N/A')}
- Gender: {data.get('gender', 'N/A')}
- Height: {height_cm} cm
- Weight: {weight_kg} kg
{f'- {bmi_str}' if bmi_str else ''}
- Symptoms: {symptoms}
- Symptom Duration: {data.get('duration', 'N/A')}
- Pain/Discomfort Level: {data.get('pain_level', 'N/A')}/10
- Existing Medical Conditions: {conditions}
- Current Medications: {medications}
- Additional Notes: {additional}

Provide your analysis in the following JSON format ONLY. Do not include any text before or after the JSON:

{{
    "overall_severity": "Low | Moderate | High | Critical",
    "health_score": <number 0-100, where 100 is perfectly healthy>,
    "summary": "<2-3 sentence overview of the assessment>",
    "possible_conditions": [
        {{
            "name": "<condition name>",
            "likelihood": "Low | Moderate | High",
            "description": "<detailed explanation of this condition in simple, clear, and very easy-to-understand English for a layperson. Avoid complex medical jargon, or define it clearly.>"
        }}
    ],
    "prescription": {{
        "doctor_notes": "<general medical notes or clinical advice from an advisory doctor in simple English>",
        "medications": [
            {{
                "name": "<medicine name, e.g. Paracetamol or Ibuprofen>",
                "dosage": "<dosage amount, e.g. 500 mg or 1 pill>",
                "frequency": "<when and how to take it, e.g. Twice daily after meals, or Once at night before sleeping>",
                "duration": "<how many days, e.g. 5 days, or As needed>",
                "instructions": "<special instructions, e.g. take with water, avoid alcohol, do not crush>"
            }}
        ]
    }},
    "general_information": "<paragraph explaining the symptoms in simple terms>",
    "recommended_actions": [
        "<action 1>",
        "<action 2>"
    ],
    "commonly_used_treatments": [
        {{
            "name": "<treatment/medication name>",
            "type": "OTC Medication | Prescription | Lifestyle | Home Remedy",
            "description": "<brief description>",
            "pros": ["<pro 1>", "<pro 2>"],
            "cons": ["<con 1>", "<con 2>"]
        }}
    ],
    "warning_signs": [
        "<warning sign that needs immediate attention>"
    ],
    "when_to_see_doctor": [
        "<specific scenario when they should see a doctor>"
    ],
    "lifestyle_recommendations": [
        "<lifestyle suggestion>"
    ],
    "disclaimer": "This is AI-generated health information for educational purposes only. It is not a medical diagnosis. Always consult a qualified healthcare professional for medical advice."
}}
"""


def _parse_response(text: str) -> dict[str, Any]:
    """Extract and parse JSON from the Gemini response text.

    The model may wrap JSON in markdown code fences — this handles that.
    """
    # Try to extract JSON from code fences first
    json_match = re.search(r"```(json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    json_str = json_match.group(2).strip() if json_match else text.strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Last resort: try to find the outermost { ... }
        brace_match = re.search(r"\{.*\}", json_str, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass

        # If all parsing fails, return a structured error response
        return {
            "overall_severity": "Moderate",
            "health_score": 50,
            "summary": "The AI analysis could not be fully parsed. Please review the raw output below.",
            "raw_response": text,
            "possible_conditions": [],
            "prescription": {
                "doctor_notes": "Unable to parse prescription details. Please consult a qualified doctor.",
                "medications": []
            },
            "general_information": text,
            "recommended_actions": ["Consult a healthcare professional for accurate assessment."],
            "commonly_used_treatments": [],
            "warning_signs": ["Unable to parse — seek professional advice."],
            "when_to_see_doctor": ["If symptoms persist or worsen."],
            "lifestyle_recommendations": [],
            "disclaimer": "AI-generated information. Not a medical diagnosis.",
        }
