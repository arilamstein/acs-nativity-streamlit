import acs_nativity
import streamlit as st

import data_access as data
import ui as ui
import visualizations as viz

st.header("U.S. Foreign‑Born Population Trends")
st.markdown(
    """
    Explore how the US foreign-born and native-born populations have changed over time.
    """
)

line_tab, bar_tab, compare_tab, ranking_tab, about_tab = st.tabs(
    ["📈 Trend", "📊 Annual Change", "🔍 Compare Years", "🏆 Ranking", "ℹ️ About"]
)
with line_tab:
    location, column = ui.location_and_demographic_block("line")
    df = data.get_data_for_name(location)
    fig = acs_nativity.plot_nativity_timeseries(df, column)
    fig.update_layout(dragmode=False)  # Disable zoom, as it causes problems on mobile
    st.plotly_chart(fig)

    # Show the same data as a table. Useful eg. if someone wants to download the data.
    st.dataframe(
        data.style_nativity_table(df[["Name", "Year", column]]), hide_index=True
    )
    st.caption("Tip: click a column header to sort.")

with bar_tab:
    location, column = ui.location_and_demographic_block("bar")
    df = data.get_data_for_name(location)
    fig = acs_nativity.plot_nativity_change(df, column)
    fig.update_layout(dragmode=False)  # Disable zoom, as it causes problems on mobile
    st.plotly_chart(fig)
    # Show the same data as a table. Useful eg. if someone wants to download the data.
    st.dataframe(
        data.style_nativity_table(df[["Name", "Year", column]]), hide_index=True
    )

with compare_tab:
    years = data.get_years()
    col1, col2, col3, col4 = st.columns([35, 35, 15, 15])
    with col1:
        location = ui.location_selector("compare")
    with col2:
        column = st.selectbox(
            "Demographic:",
            options=ui.get_demographic_options(),
            index=ui.get_demographic_options().index("Percent Foreign-born"),
            key="compare_column_selector",
        )
    with col3:
        year1 = st.selectbox("First Year:", years, 0)
    with col4:
        year2 = st.selectbox("Second Year:", years, len(years) - 1)

    if column != "Percent Foreign-born":
        plot_column = st.radio(
            "Unit:",
            options=["Population", "Percent Change"],
            index=0,
            horizontal=True,
        )
        if plot_column == "Population":
            plot_column = "Change"
    else:
        plot_column = "Change (pct points)"

    # Chart followed by table
    st.plotly_chart(
        viz.get_compare_scatterplot(year1, year2, column, plot_column, location)
    )
    st.dataframe(
        data.get_compare_df_styled(year1, year2, column, plot_column),
        hide_index=True,
    )

with ranking_tab:
    col1, col2, col3 = st.columns([40, 40, 20])
    with col1:
        location = ui.location_selector("ranking")
    with col2:
        column = st.selectbox(
            "Demographic:",
            options=ui.get_demographic_options(),
            index=ui.get_demographic_options().index("Percent Foreign-born"),
            key="table_column_selector",
        )
    with col3:
        years = data.get_years()
        year = st.selectbox("Year:", data.get_years(), len(years) - 1)

    # Chart followed by table
    st.plotly_chart(viz.get_ranking_scatterplot(year, column, location))
    st.dataframe(data.get_table_df_styled(year, column), hide_index=True)

with about_tab, open("about.md") as f:
    st.write(f.read())
