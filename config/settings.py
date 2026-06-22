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
ENV_FILE: Final[Path] = PROJECT_ROOT / ".env"

# Ensure critical directories exist at import time
REPORTS_DIR.mkdir(exist_ok=True)


def _load_local_env_file() -> None:
    """Load simple KEY=VALUE pairs from the project .env file if it exists."""
    if not ENV_FILE.exists():
        return

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_local_env_file()

# ─── Application Metadata ────────────────────────────────────────────────────
APP_NAME: Final[str] = "Health Companion"
APP_VERSION: Final[str] = "1.0.0"
APP_DESCRIPTION: Final[str] = (
    "Health assessment and report assistant — "
    "Get structured health insights when you need a quick check-in."
)
APP_ICON: Final[str] = "◼"

# ─── Gemini Configuration ────────────────────────────────────────────────────
GEMINI_MODEL: Final[str] = "gemini-2.5-flash"

def get_gemini_api_key() -> str | None:
    """Return the Gemini API key from env var or None."""
    return os.environ.get("GEMINI_API_KEY")

# ─── Color Palette ────────────────────────────────────────────────────────────
# Light Green Skeuomorphism

class Colors:
    """Design-token color constants used across UI components."""

    # Primary
    PRIMARY: Final[str] = "#23436A"
    PRIMARY_LIGHT: Final[str] = "#4E739B"
    PRIMARY_DARK: Final[str] = "#172A45"

    # Accent
    ACCENT: Final[str] = "#23436A"
    ACCENT_LIGHT: Final[str] = "#4E739B"

    # Semantic
    SUCCESS: Final[str] = "#22C55E"
    WARNING: Final[str] = "#EAB308"
    DANGER: Final[str] = "#DC2626"
    INFO: Final[str] = "#2563EB"

    # Neutrals (Light green-tinted)
    BG_PRIMARY: Final[str] = "#F5F3EF"
    BG_SECONDARY: Final[str] = "#FBFAF8"
    BG_CARD: Final[str] = "rgba(255, 255, 255, 0.78)"
    BORDER: Final[str] = "rgba(19, 31, 45, 0.10)"
    TEXT_PRIMARY: Final[str] = "#17212E"
    TEXT_SECONDARY: Final[str] = "#4B5563"
    TEXT_MUTED: Final[str] = "#6B7280"

    # Gradients
    GRADIENT_PRIMARY: Final[str] = "linear-gradient(135deg, #23436A 0%, #4E739B 100%)"
    GRADIENT_SUCCESS: Final[str] = "linear-gradient(135deg, #4E739B 0%, #23436A 100%)"
    GRADIENT_DANGER: Final[str] = "linear-gradient(135deg, #EF4444 0%, #DC2626 100%)"
    GRADIENT_WARM: Final[str] = "linear-gradient(135deg, #EAB308 0%, #DC2626 100%)"

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
    "**Medical Disclaimer**: Health Companion is an informational tool "
    "and does **NOT** provide medical diagnoses or treatment recommendations. "
    "The information generated should **never** replace professional medical advice, "
    "diagnosis, or treatment. Always consult a qualified healthcare provider for "
    "medical concerns. In case of emergency, contact your local emergency services immediately."
)

# ─── Navigation ───────────────────────────────────────────────────────────────

NAV_ITEMS: Final[list[dict[str, str]]] = [
    {"key": "dashboard",   "label": "Dashboard",         "icon": ""},
    {"key": "assessment",  "label": "Health Assessment",  "icon": ""},
    {"key": "analysis",    "label": "Analysis",           "icon": ""},
    {"key": "reports",     "label": "Previous Reports",   "icon": ""},
    {"key": "settings",    "label": "Settings",           "icon": ""},
]
