import numpy as np
import plotly.graph_objects as go

import data_access as da


def _add_source_footer(
    fig: go.Figure,
    source_text: str = "Source: American Community Survey 1-Year Estimates",
) -> None:
    fig.add_annotation(
        text=source_text,
        x=0,
        y=-0.15,
        xref="paper",
        yref="paper",
        showarrow=False,
        xanchor="left",
        yanchor="top",
        align="left",
        font=dict(size=12, color="gray"),
    )


def _get_ranking_hovertext(column: str) -> str:
    if column.startswith("Percent"):
        value_fmt = f"{column}: %{{customdata[1]:,.1f}}%"
    else:
        value_fmt = f"{column}: %{{customdata[1]:,}}"
    return (
        "%{customdata[0]}<br>"  # Line 1: location name
        f"{value_fmt}"  # Line 2: column name and value (Plotly %{} syntax)
        "<extra></extra>"  # Suppress trace name box
    )


def get_table_scatterplot(state: str, latest_only: bool, column: str) -> go.Figure:

    df = da.get_table_df(state, latest_only, column)

    fig = go.Figure()

    # A scatterplot with jitter
    rng = np.random.default_rng(seed=42)
    jitter = rng.uniform(-0.3, 0.3, size=len(df))
    fig.add_trace(
        go.Scatter(
            y=df[column],
            x=jitter,
            mode="markers",
            marker=dict(size=8, opacity=0.5),
            customdata=df[["Name", column]].values,
            hovertemplate=_get_ranking_hovertext(column),
            name=column,
            showlegend=False,
        )
    )

    # Title and footer
    fig.update_layout(
        title=(
            f"{column}<br><sup>Each point represents a location. "
            "Hover to explore.</sup>"
        ),
        xaxis=dict(visible=False, range=[-1, 1]),
        yaxis=dict(title=column, tickformat=","),
    )
    _add_source_footer(fig)

    return fig


def _get_compare_hovertext(plot_column: str) -> str:
    if plot_column == "Change":
        return (
            "%{customdata[0]}<br>"  # Line 1: location
            # Line 2: format with 1 decimal point and trailing %
            f"{plot_column}: %{{customdata[1]:,.0f}}"
            "<extra></extra>"  # Suppress trace name
        )
    elif plot_column == "Percent Change" or plot_column == "Change (pct points)":
        return (
            "%{customdata[0]}<br>"  # Line 1: location
            # Line 2: format with 1 decimal point and trailing %
            f"{plot_column}: %{{customdata[1]:,.1f}}%"
            "<extra></extra>"  # Suppress trace name
        )
    else:
        raise ValueError(f"Unexpected plot_column: {plot_column}")


def get_compare_scatterplot(
    state: str, year1: int, year2: int, orig_column: str, plot_column: str
) -> go.Figure:
    fig = go.Figure()

    df = da.get_compare_df(state, year1, year2, orig_column, plot_column).reset_index(
        drop=True
    )
    if orig_column == "Percent Foreign-born":
        plot_column = "Change (pct points)"

    # A scatterplot with jitter
    rng = np.random.default_rng(seed=42)
    jitter = rng.uniform(-0.25, 0.25, size=len(df))
    fig.add_trace(
        go.Scatter(
            y=df[plot_column],
            x=jitter,
            mode="markers",
            marker=dict(size=8, opacity=0.5),
            customdata=df[["Name", plot_column]].values,
            hovertemplate=_get_compare_hovertext(plot_column),
            name=plot_column,
            showlegend=False,
        )
    )

    # Title and footer
    if orig_column == "Percent Foreign-born":
        title = f"Change in Percent Foreign-born, {year1}–{year2}"
        y_title = "Percentage Points"
    else:
        title = f"{plot_column} in {orig_column}, {year1}–{year2}"
        y_title = "Population" if plot_column == "Change" else plot_column
    fig.update_layout(
        title=(
            f"{title}<br><sup>Each point represents a location. Hover to explore.</sup>"
        ),
        xaxis=dict(visible=False, range=[-1, 1]),
        yaxis=dict(title=y_title, tickformat=","),
    )
    _add_source_footer(fig)

    return fig
