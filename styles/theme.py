"""
HealthAI Pro — Premium Theme Engine

Injects custom CSS into Streamlit for a neumorphic / glassmorphic
Apple-HIG-inspired medical dashboard look.
"""

from __future__ import annotations

import streamlit as st


def inject_theme() -> None:
    """Inject the complete premium CSS theme into the Streamlit app."""
    st.markdown(_GOOGLE_FONTS_LINK, unsafe_allow_html=True)
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


# ─── Google Fonts ─────────────────────────────────────────────────────────────

_GOOGLE_FONTS_LINK: str = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
      rel="stylesheet">
"""

# ─── Master CSS ───────────────────────────────────────────────────────────────

_CSS: str = """
/* ═══════════════════════════════════════════════════════════════════════
   HEALTHAI PRO — PREMIUM THEME
   ═══════════════════════════════════════════════════════════════════════ */

/* ─── Root Variables ────────────────────────────────────────────────── */
:root {
    --primary: #0EA5E9;
    --primary-light: #38BDF8;
    --primary-dark: #0284C7;
    --accent: #8B5CF6;
    --accent-light: #A78BFA;
    --success: #22C55E;
    --warning: #F59E0B;
    --danger: #EF4444;
    --bg-primary: #F8FAFC;
    --bg-secondary: #F1F5F9;
    --bg-card: rgba(255, 255, 255, 0.72);
    --border: #E2E8F0;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
    --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04);
    --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.07), 0 2px 4px rgba(15, 23, 42, 0.04);
    --shadow-lg: 0 10px 30px rgba(15, 23, 42, 0.08), 0 4px 8px rgba(15, 23, 42, 0.04);
    --shadow-neu: 6px 6px 14px rgba(15, 23, 42, 0.07), -6px -6px 14px rgba(255, 255, 255, 0.9);
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 20px;
    --radius-xl: 28px;
    --blur: 18px;
    --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ─── Global Reset ──────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    color: var(--text-primary);
}

/* ─── Main Container ────────────────────────────────────────────────── */
.stApp {
    background: var(--bg-primary) !important;
}

.main .block-container {
    max-width: 1200px;
    padding: 2rem 2.5rem 4rem 2.5rem !important;
}

/* ─── Sidebar ───────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 12px rgba(15, 23, 42, 0.04) !important;
}

section[data-testid="stSidebar"] .stMarkdown h1 {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #0EA5E9, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}

section[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
}

/* ─── Sidebar Buttons (navigation) ──────────────────────────────────── */
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    text-align: left !important;
    justify-content: flex-start !important;
    background: transparent !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.7rem 1rem !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    color: var(--text-secondary) !important;
    transition: var(--transition) !important;
    box-shadow: none !important;
    margin-bottom: 2px !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg-secondary) !important;
    color: var(--primary) !important;
    transform: translateX(3px);
}

/* Active nav item is handled by adding a custom class via markdown */

/* ─── Glass Card ────────────────────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    transition: var(--transition);
}

.glass-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

/* ─── Neumorphic Card ───────────────────────────────────────────────── */
.neu-card {
    background: #FFFFFF;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-neu);
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(226, 232, 240, 0.5);
    transition: var(--transition);
}

.neu-card:hover {
    box-shadow: 8px 8px 18px rgba(15, 23, 42, 0.09), -8px -8px 18px rgba(255, 255, 255, 1);
    transform: translateY(-2px);
}

/* ─── Metric Cards ──────────────────────────────────────────────────── */
.metric-card {
    background: #FFFFFF;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    padding: 1.4rem 1.6rem;
    border: 1px solid var(--border);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.metric-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-3px);
}

.metric-card .metric-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.metric-card .metric-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1.1;
}

.metric-card .metric-label {
    font-size: 0.82rem;
    color: var(--text-muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.25rem;
}

/* Accent top-border colors */
.metric-card.mc-primary::before   { background: linear-gradient(90deg, #0EA5E9, #38BDF8); }
.metric-card.mc-accent::before    { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
.metric-card.mc-success::before   { background: linear-gradient(90deg, #22C55E, #4ADE80); }
.metric-card.mc-warning::before   { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
.metric-card.mc-danger::before    { background: linear-gradient(90deg, #EF4444, #F87171); }

/* ─── Page Header ───────────────────────────────────────────────────── */
.page-header {
    background: linear-gradient(135deg, #0EA5E9 0%, #8B5CF6 100%);
    border-radius: var(--radius-xl);
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    color: white;
    position: relative;
    overflow: hidden;
}

.page-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 50%;
}

.page-header::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: 10%;
    width: 200px;
    height: 200px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 50%;
}

.page-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 0.25rem 0;
    color: white !important;
    letter-spacing: -0.02em;
    position: relative;
    z-index: 1;
}

.page-header p {
    margin: 0;
    font-size: 0.95rem;
    opacity: 0.9;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* ─── Severity Badges ───────────────────────────────────────────────── */
.severity-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.badge-low      { background: #DCFCE7; color: #166534; }
.badge-moderate { background: #FEF3C7; color: #92400E; }
.badge-high     { background: #FEE2E2; color: #991B1B; }
.badge-critical { background: #7F1D1D; color: #FECACA; }

/* ─── Form Inputs ───────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: var(--radius-md) !important;
    border: 1.5px solid var(--border) !important;
    padding: 0.65rem 1rem !important;
    font-family: var(--font) !important;
    font-size: 0.92rem !important;
    transition: var(--transition) !important;
    background: #FFFFFF !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.12) !important;
}

/* ─── Select Boxes ──────────────────────────────────────────────────── */
.stSelectbox > div > div {
    border-radius: var(--radius-md) !important;
    border: 1.5px solid var(--border) !important;
    transition: var(--transition) !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.12) !important;
}

/* ─── Buttons ───────────────────────────────────────────────────────── */
.stButton > button {
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    font-family: var(--font) !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.6rem !important;
    transition: var(--transition) !important;
    letter-spacing: 0.01em !important;
}

/* Primary button */
.stButton > button[kind="primary"],
.main .stButton > button:not([kind]) {
    background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3) !important;
}

.stButton > button[kind="primary"]:hover,
.main .stButton > button:not([kind]):hover {
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* ─── Tabs ──────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm);
    font-weight: 500;
    font-family: var(--font);
    transition: var(--transition);
    padding: 0.5rem 1rem;
}

.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: var(--shadow-sm);
    font-weight: 600;
}

/* ─── Expanders ─────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    border-radius: var(--radius-md) !important;
}

details {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    background: white !important;
}

/* ─── Progress Bar ──────────────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #0EA5E9, #8B5CF6) !important;
    border-radius: 999px !important;
}

/* ─── Divider ───────────────────────────────────────────────────────── */
hr {
    border: none !important;
    height: 1px !important;
    background: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ─── Alerts / Info boxes ───────────────────────────────────────────── */
.stAlert {
    border-radius: var(--radius-md) !important;
    font-family: var(--font) !important;
}

/* ─── Disclaimer Banner ─────────────────────────────────────────────── */
.disclaimer-banner {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    border: 1px solid #F59E0B;
    border-radius: var(--radius-md);
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #92400E;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

/* ─── Wizard Progress ───────────────────────────────────────────────── */
.wizard-steps {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 2rem;
    padding: 0 0.5rem;
}

.wizard-step {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
    position: relative;
}

.wizard-step .step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    flex-shrink: 0;
    transition: var(--transition);
}

.wizard-step .step-label {
    font-size: 0.78rem;
    font-weight: 500;
    white-space: nowrap;
}

.wizard-step.active .step-circle {
    background: linear-gradient(135deg, #0EA5E9, #0284C7);
    color: white;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.35);
}

.wizard-step.active .step-label {
    color: var(--primary);
    font-weight: 600;
}

.wizard-step.completed .step-circle {
    background: var(--success);
    color: white;
}

.wizard-step.completed .step-label {
    color: var(--success);
}

.wizard-step.pending .step-circle {
    background: var(--bg-secondary);
    color: var(--text-muted);
    border: 2px solid var(--border);
}

.wizard-step.pending .step-label {
    color: var(--text-muted);
}

.wizard-connector {
    flex: 1;
    height: 2px;
    background: var(--border);
    margin: 0 0.3rem;
}

.wizard-connector.completed {
    background: var(--success);
}

/* ─── Animations ────────────────────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeInUp 0.5s ease-out both;
}

.animate-in-1 { animation-delay: 0.05s; }
.animate-in-2 { animation-delay: 0.12s; }
.animate-in-3 { animation-delay: 0.19s; }
.animate-in-4 { animation-delay: 0.26s; }

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.3); }
    50%      { box-shadow: 0 0 0 10px rgba(14, 165, 233, 0); }
}

.pulse-glow {
    animation: pulse-glow 2s ease-in-out infinite;
}

/* ─── Scrollbar ─────────────────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: var(--text-muted);
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}

/* ─── Utility: Hide default Streamlit chrome ────────────────────────── */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }
"""
