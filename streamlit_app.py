import streamlit as st
import acs_nativity
import data_access as data

st.title("U.S. Foreign‑Born Population Trends")
st.markdown(
    """
    Explore how the foreign‑born and native‑born populations have changed 
    across the United States since 2005.  
    **Start typing** the name of a State, County, or City to search for it.
    """
)

# Let user select what data they want to see.
col1, col2 = st.columns(2)
with col1:
    location_options = data.get_all_names()
    location = st.selectbox(
        label="Location:",
        options=location_options,
        index=None,
        placeholder="Search for a place...",
    )
    st.markdown("_(Tip: start typing to filter the list)_")
with col2:
    column = st.selectbox(
        "Demographic:",
        options=["Foreign-born", "Percent Foreign-born", "Native", "Total"],
    )

if location is None:
    location = "United States"
df = data.get_data_for_name(location)

# Make charts
line_tab, bar_tab, table_tab, compare_tab, about_tab = st.tabs(
    ["📈 Trend", "📊 Year‑to‑Year Change", "📋 Table", "🔍 Compare Years", "ℹ️ About"]
)
with line_tab:
    st.plotly_chart(acs_nativity.plot_nativity_timeseries(df, column))

with bar_tab:
    st.plotly_chart(acs_nativity.plot_nativity_change(df, column))

with table_tab:
    latest_only = st.checkbox("Latest year only", True)
    year_text = "the **latest year**" if latest_only else "**all years**"
    st.markdown(f"Showing all geographies for {year_text}.")

    st.dataframe(data.get_table_df_styled(latest_only), hide_index=True)

with compare_tab:
    years = data.get_years()
    col1, col2 = st.columns(2)
    with col1:
        year1 = st.selectbox("First Year:", years, 0)
    with col2:
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
    st.dataframe(data.get_compare_df_styled(year1, year2, column), hide_index=True)

with about_tab:
    st.write(open("about.md").read())
