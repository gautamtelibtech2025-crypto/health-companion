"""
HealthAI Pro — Form Components

Styled wrapper functions for Streamlit form inputs.
These are thin convenience wrappers — no custom HTML injection,
just consistent default arguments.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def styled_text_input(
    label: str,
    *,
    key: str | None = None,
    value: str = "",
    placeholder: str = "",
    help: str | None = None,
    type: str = "default",
) -> str:
    """Streamlit text_input with sensible defaults."""
    return st.text_input(
        label,
        value=value,
        placeholder=placeholder,
        help=help,
        key=key,
        type=type,
    )


def styled_number_input(
    label: str,
    *,
    key: str | None = None,
    min_value: float | int | None = None,
    max_value: float | int | None = None,
    value: float | int | None = None,
    step: float | int | None = None,
    help: str | None = None,
) -> float | int:
    """Streamlit number_input with sensible defaults."""
    return st.number_input(
        label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step,
        help=help,
        key=key,
    )


def styled_selectbox(
    label: str,
    options: list[str],
    *,
    key: str | None = None,
    index: int = 0,
    help: str | None = None,
) -> str:
    """Streamlit selectbox with sensible defaults."""
    return st.selectbox(
        label,
        options,
        index=index,
        help=help,
        key=key,
    )


def styled_multiselect(
    label: str,
    options: list[str],
    *,
    key: str | None = None,
    default: list[str] | None = None,
    help: str | None = None,
    max_selections: int | None = None,
) -> list[str]:
    """Streamlit multiselect with sensible defaults."""
    kwargs: dict[str, Any] = {
        "label": label,
        "options": options,
        "default": default or [],
        "help": help,
        "key": key,
    }
    if max_selections is not None:
        kwargs["max_selections"] = max_selections
    return st.multiselect(**kwargs)


def styled_slider(
    label: str,
    *,
    key: str | None = None,
    min_value: int | float = 0,
    max_value: int | float = 10,
    value: int | float = 5,
    step: int | float = 1,
    help: str | None = None,
) -> int | float:
    """Streamlit slider with sensible defaults."""
    return st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step,
        help=help,
        key=key,
    )


def styled_text_area(
    label: str,
    *,
    key: str | None = None,
    value: str = "",
    placeholder: str = "",
    height: int = 120,
    help: str | None = None,
) -> str:
    """Streamlit text_area with sensible defaults."""
    return st.text_area(
        label,
        value=value,
        placeholder=placeholder,
        height=height,
        help=help,
        key=key,
    )


def wizard_progress(current_step: int, steps: list[str]) -> None:
    """Render a multi-step wizard progress bar using HTML.

    Args:
        current_step: 1-indexed current step number.
        steps: List of step label strings.
    """
    parts: list[str] = []
    for idx, label in enumerate(steps, 1):
        if idx < current_step:
            state = "completed"
            circle_content = "✓"
        elif idx == current_step:
            state = "active"
            circle_content = str(idx)
        else:
            state = ""
            circle_content = str(idx)

        parts.append(
            f'<div class="wizard-step {state}">'
            f'  <div class="step-circle">{circle_content}</div>'
            f'  <div class="step-label">{label}</div>'
            f"</div>"
        )

        # Connector between steps (not after last)
        if idx < len(steps):
            conn_state = "completed" if idx < current_step else ""
            parts.append(f'<div class="wizard-connector {conn_state}"></div>')

    st.markdown(
        f'<div class="wizard-steps animate-in">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )
