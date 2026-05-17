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
        dragmode=False,
    )
    _add_source_footer(fig)

    return fig


# def _get_compare_hovertext() -> str:
#     return (
#         "%{customdata[0]}<br>"  # Line 1: location
#         # Line 2: format with 1 decimal point and trailing %
#         "Percent Change: %{customdata[1]:,.1f}%"
#         "<extra></extra>"  # Suppress trace name
#     )


# def get_compare_scatterplot(state, year1, year2, column):
#     fig = go.Figure()

#     name_to_highlight = "United States"

#     df = da.get_compare_df(state, year1, year2, column).reset_index(drop=True)
#     if column == "Percent Foreign-born":
#         column = "Change (pct points)"
#     st.write(df.columns)
#     #    return
#     # A scatterplot with jitter
#     rng = np.random.default_rng(seed=42)
#     jitter = rng.uniform(-0.25, 0.25, size=len(df))
#     fig.add_trace(
#         go.Scatter(
#             # y=df["Percent Change"],
#             y=df[column],
#             x=jitter,
#             mode="markers",
#             marker=dict(size=8, opacity=0.5),
#             # customdata=df[["Name", "Percent Change"]].values,
#             customdata=df[["Name", column]].values,
#             hovertemplate=_get_compare_hovertext(),
#             name="Percent Change",
#             showlegend=False,
#         )
#     )

#     # Optionally put a star to highlight a point
#     if name_to_highlight:
#         hdf = df[df["Name"] == name_to_highlight]

#         fig.add_trace(
#             go.Scatter(
#                 x=[0],
#                 #                y=hdf["Percent Change"],
#                 y=hdf[column],
#                 mode="markers",
#                 marker=dict(
#                     color="gold",
#                     size=14,
#                     symbol="star",
#                     line=dict(color="darkorange", width=1.5),
#                 ),
#                 name=name_to_highlight,
#                 # customdata=hdf[["Name", "Percent Change"]].values,
#                 customdata=hdf[["Name", column]].values,
#                 hovertemplate=_get_compare_hovertext(),
#             )
#         )

#     # Title and footer
#     fig.update_layout(
#         title=(
#             f"Percent Change in {column}, {year1}–{year2}<br>"
#             "<sup>Each point represents a location. Hover to explore.</sup>"
#         ),
#         xaxis=dict(visible=False, range=[-1, 1]),
#         yaxis=dict(title="Percent Change", tickformat=","),
#         dragmode=False,
#     )
#     _add_source_footer(fig)

#     return fig
