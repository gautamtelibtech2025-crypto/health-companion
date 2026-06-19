"""
HealthAI Pro — Application Configuration & Constants

Central configuration file for colors, typography, symptom lists,
severity levels, and Gemini model settings.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

# ─── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
REPORTS_DIR: Final[Path] = PROJECT_ROOT / "reports"
ASSETS_DIR: Final[Path] = PROJECT_ROOT / "assets"

# Ensure critical directories exist at import time
REPORTS_DIR.mkdir(exist_ok=True)

# ─── Application Metadata ────────────────────────────────────────────────────
APP_NAME: Final[str] = "HealthAI Pro"
APP_VERSION: Final[str] = "1.0.0"
APP_DESCRIPTION: Final[str] = (
    "AI-Powered Health Assessment Assistant — "
    "Get preliminary health insights powered by Google Gemini."
)
APP_ICON: Final[str] = "🏥"

# ─── Gemini Configuration ────────────────────────────────────────────────────
GEMINI_MODEL: Final[str] = "gemini-2.5-flash"

def get_gemini_api_key() -> str | None:
    """Return the Gemini API key from env var or None."""
    return os.environ.get("GEMINI_API_KEY")

# ─── Color Palette ────────────────────────────────────────────────────────────
# Inspired by medical / healthcare branding — clean blues, teals, slates.

class Colors:
    """Design-token color constants used across UI components."""

    # Primary
    PRIMARY: Final[str] = "#0EA5E9"       # Sky-500
    PRIMARY_LIGHT: Final[str] = "#38BDF8" # Sky-400
    PRIMARY_DARK: Final[str] = "#0284C7"  # Sky-600

    # Accent
    ACCENT: Final[str] = "#8B5CF6"        # Violet-500
    ACCENT_LIGHT: Final[str] = "#A78BFA"  # Violet-400

    # Semantic
    SUCCESS: Final[str] = "#22C55E"       # Green-500
    WARNING: Final[str] = "#F59E0B"       # Amber-500
    DANGER: Final[str] = "#EF4444"        # Red-500
    INFO: Final[str] = "#3B82F6"          # Blue-500

    # Neutrals (Slate palette)
    BG_PRIMARY: Final[str] = "#F8FAFC"    # Slate-50
    BG_SECONDARY: Final[str] = "#F1F5F9"  # Slate-100
    BG_CARD: Final[str] = "rgba(255, 255, 255, 0.72)"
    BORDER: Final[str] = "#E2E8F0"        # Slate-200
    TEXT_PRIMARY: Final[str] = "#0F172A"   # Slate-900
    TEXT_SECONDARY: Final[str] = "#475569" # Slate-500
    TEXT_MUTED: Final[str] = "#94A3B8"     # Slate-400

    # Gradients
    GRADIENT_PRIMARY: Final[str] = "linear-gradient(135deg, #0EA5E9 0%, #8B5CF6 100%)"
    GRADIENT_SUCCESS: Final[str] = "linear-gradient(135deg, #22C55E 0%, #16A34A 100%)"
    GRADIENT_DANGER: Final[str] = "linear-gradient(135deg, #EF4444 0%, #DC2626 100%)"
    GRADIENT_WARM: Final[str] = "linear-gradient(135deg, #F59E0B 0%, #EF4444 100%)"

# ─── Severity Levels ─────────────────────────────────────────────────────────

SEVERITY_LEVELS: Final[dict[str, dict[str, str]]] = {
    "Low": {
        "color": Colors.SUCCESS,
        "icon": "🟢",
        "label": "Low Severity",
        "description": "Minor issue — likely manageable with self-care.",
    },
    "Moderate": {
        "color": Colors.WARNING,
        "icon": "🟡",
        "label": "Moderate Severity",
        "description": "Should be monitored — consider consulting a doctor.",
    },
    "High": {
        "color": Colors.DANGER,
        "icon": "🔴",
        "label": "High Severity",
        "description": "Potentially serious — seek medical attention promptly.",
    },
    "Critical": {
        "color": "#7F1D1D",
        "icon": "🚨",
        "label": "Critical",
        "description": "Urgent — seek emergency medical care immediately.",
    },
}

# ─── Symptom & Condition Lists ───────────────────────────────────────────────

COMMON_SYMPTOMS: Final[list[str]] = [
    "Headache",
    "Fever",
    "Cough",
    "Sore Throat",
    "Fatigue",
    "Body Aches",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Shortness of Breath",
    "Chest Pain",
    "Dizziness",
    "Back Pain",
    "Joint Pain",
    "Abdominal Pain",
    "Skin Rash",
    "Runny Nose",
    "Congestion",
    "Loss of Appetite",
    "Difficulty Sleeping",
    "Anxiety",
    "Swelling",
    "Numbness / Tingling",
    "Vision Changes",
    "Ear Pain",
    "Frequent Urination",
    "Weight Loss (unexplained)",
    "Weight Gain (unexplained)",
]

EXISTING_CONDITIONS: Final[list[str]] = [
    "Diabetes (Type 1)",
    "Diabetes (Type 2)",
    "Hypertension",
    "Asthma",
    "Heart Disease",
    "Thyroid Disorder",
    "Arthritis",
    "COPD",
    "Depression / Anxiety",
    "Kidney Disease",
    "Liver Disease",
    "Cancer (any type)",
    "Epilepsy",
    "Anemia",
    "Allergies (specify in notes)",
    "None",
]

GENDER_OPTIONS: Final[list[str]] = [
    "Male",
    "Female",
    "Non-binary",
    "Prefer not to say",
]

DURATION_OPTIONS: Final[list[str]] = [
    "Less than 24 hours",
    "1–3 days",
    "4–7 days",
    "1–2 weeks",
    "2–4 weeks",
    "More than a month",
    "Chronic / Recurring",
]

# ─── Medical Disclaimer ──────────────────────────────────────────────────────

DISCLAIMER: Final[str] = (
    "⚕️ **Medical Disclaimer**: HealthAI Pro is an AI-powered informational tool "
    "and does **NOT** provide medical diagnoses or treatment recommendations. "
    "The information generated should **never** replace professional medical advice, "
    "diagnosis, or treatment. Always consult a qualified healthcare provider for "
    "medical concerns. In case of emergency, contact your local emergency services immediately."
)

# ─── Navigation ───────────────────────────────────────────────────────────────

NAV_ITEMS: Final[list[dict[str, str]]] = [
    {"key": "dashboard",   "label": "Dashboard",         "icon": "📊"},
    {"key": "assessment",  "label": "Health Assessment",  "icon": "🩺"},
    {"key": "analysis",    "label": "AI Analysis",        "icon": "🧠"},
    {"key": "reports",     "label": "Previous Reports",   "icon": "📄"},
    {"key": "settings",    "label": "Settings",           "icon": "⚙️"},
]
