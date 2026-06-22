"""
HealthAI Pro — Metric & Chart Components

Dashboard metric rows and Plotly gauge charts.
"""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

from config.settings import Colors


def metric_row(metrics: list[dict[str, str]]) -> None:
    """Render a horizontal row of metric cards.

    Args:
        metrics: List of dicts with keys 'icon', 'value', 'label', 'accent'.
                 The icon value is accepted for compatibility but not shown.
    """
    cols = st.columns(len(metrics))
    for idx, (col, m) in enumerate(zip(cols, metrics)):
        accent = m.get("accent", "primary")
        anim = f"animate-in-{min(idx + 1, 4)}"
        with col:
            st.markdown(
                f"""
                <div class="metric-card mc-{accent} animate-in {anim}">
                    <div class="metric-icon" aria-hidden="true">&nbsp;</div>
                    <div class="metric-value">{m['value']}</div>
                    <div class="metric-label">{m['label']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def health_score_gauge(score: int, title: str = "Health Score") -> go.Figure:
    """Create a Plotly gauge chart for a 0–100 health score.

    Args:
        score: Numeric health score (0–100).
        title: Chart title.

    Returns:
        A plotly Figure object — render with st.plotly_chart().
    """
    if score >= 80:
        bar_color = Colors.SUCCESS
    elif score >= 50:
        bar_color = Colors.WARNING
    else:
        bar_color = Colors.DANGER

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "", "font": {"size": 48, "family": "Inter", "color": Colors.TEXT_PRIMARY}},
            title={"text": title, "font": {"size": 16, "family": "Inter", "color": Colors.TEXT_SECONDARY}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 0,
                    "tickcolor": "rgba(0,0,0,0)",
                    "dtick": 25,
                    "tickfont": {"size": 11, "color": Colors.TEXT_MUTED},
                },
                "bar": {"color": bar_color, "thickness": 0.75},
                "bgcolor": Colors.BG_SECONDARY,
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(239,68,68,0.08)"},
                    {"range": [40, 70], "color": "rgba(245,158,11,0.08)"},
                    {"range": [70, 100], "color": "rgba(34,197,94,0.08)"},
                ],
                "threshold": {
                    "line": {"color": bar_color, "width": 3},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )

    fig.update_layout(
        height=250,
        margin={"t": 40, "b": 10, "l": 30, "r": 30},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
    )

    return fig


def severity_distribution_chart(data: dict[str, int]) -> go.Figure:
    """Create a donut chart showing severity distribution.

    Args:
        data: Dict mapping severity level names to counts.

    Returns:
        A plotly Figure.
    """
    colors_map = {
        "Low": Colors.SUCCESS,
        "Moderate": Colors.WARNING,
        "High": Colors.DANGER,
        "Critical": "#7F1D1D",
    }

    labels = list(data.keys())
    values = list(data.values())
    colors = [colors_map.get(l, Colors.PRIMARY) for l in labels]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker={"colors": colors, "line": {"color": "#FFFFFF", "width": 2}},
            textinfo="label+percent",
            textfont={"family": "Inter", "size": 12},
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
        )
    )

    fig.update_layout(
        showlegend=False,
        height=280,
        margin={"t": 20, "b": 20, "l": 20, "r": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
    )

    return fig
