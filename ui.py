import streamlit as st
import data_access as data
import pandas as pd


def sync_value(source_key: str, target_key: str) -> None:
    st.session_state[target_key] = st.session_state[source_key]


def location_and_demographic_selector(tab: str) -> tuple[str, str, pd.DataFrame]:
    st.markdown(
        "**Start typing** the name of a State, County, or City to search for it. "
        "Or leave blank to view totals for the entire United States."
    )
    col1, col2 = st.columns(2)

    with col1:
        loc_key = f"{tab}_loc_value"
        other_loc_key = "bar_loc_value" if tab == "line" else "line_loc_value"

        location_options = data.get_all_names()
        location = st.selectbox(
            "Location:",
            options=location_options,
            placeholder="Search for a place...",
            index=None,
            key=loc_key,
            on_change=lambda: sync_value(loc_key, other_loc_key),
        )

        st.markdown("_(Tip: start typing to filter the list)_")

    with col2:
        demo_key = f"{tab}_demo_value"
        other_demo_key = "bar_demo_value" if tab == "line" else "line_demo_value"

        demographic_options = [
            "Foreign-born",
            "Percent Foreign-born",
            "Native",
            "Total",
        ]
        column = st.selectbox(
            "Demographic:",
            options=demographic_options,
            key=demo_key,
            on_change=lambda: sync_value(demo_key, other_demo_key),
        )

    if location is None:
        location = "United States"
    df = data.get_data_for_name(location)
    return location, column, df
