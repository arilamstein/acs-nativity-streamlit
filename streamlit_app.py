import streamlit as st
import acs_nativity
import data_access as data
import ui as ui

st.set_page_config(layout="wide")
st.title("U.S. Foreign‑Born Population Trends")
st.markdown(
    """
    Explore how the foreign‑born and native‑born populations have changed 
    across the United States since 2005.  
    """
)

line_tab, bar_tab, table_tab, compare_tab, about_tab = st.tabs(
    ["📈 Trend", "📊 Year‑to‑Year Change", "📋 Table", "🔍 Compare Years", "ℹ️ About"]
)
with line_tab:
    location, column, df = ui.location_and_demographic_selector("line")
    st.plotly_chart(acs_nativity.plot_nativity_timeseries(df, column))

with bar_tab:
    location, column, df = ui.location_and_demographic_selector("bar")
    st.plotly_chart(acs_nativity.plot_nativity_change(df, column))

with table_tab:
    col1, _ = st.columns([1, 2])
    with col1:
        state = ui.state_selector("table")
    latest_only = st.checkbox("Latest year only", True)
    year_text = "the **latest year**" if latest_only else "**all years**"
    st.markdown(f"Showing all geographies for **{state}** for {year_text}.")

    st.dataframe(data.get_table_df_styled(state, latest_only), hide_index=True)

with compare_tab:
    years = data.get_years()
    col1, col2, col3 = st.columns(3)
    with col1:
        state = ui.state_selector("compare")
    with col2:
        year1 = st.selectbox("First Year:", years, 0)
    with col3:
        year2 = st.selectbox("Second Year:", years, len(years) - 1)

    year_text = f"**{year1}** and **{year2}**"
    if location == "United States":
        st.markdown(
            f"Showing the change in **{column}** in the **United States** between {year_text}."
        )
    else:
        st.markdown(
            f"Showing the change in **{column}** in **{location}** between {year_text}."
        )
    st.dataframe(
        data.get_compare_df_styled(state, year1, year2, column), hide_index=True
    )

with about_tab:
    st.write(open("about.md").read())
