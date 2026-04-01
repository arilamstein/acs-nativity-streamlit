import streamlit as st
import data_access as data
import pandas as pd

VALID_TABS = ["bar", "line", "table", "compare"]


def validate_tab(tab: str) -> None:
    if tab not in VALID_TABS:
        raise ValueError(f"tab must one of {VALID_TABS}. {tab} given")


def sync_values(source_key: str, all_keys: list[str]) -> None:
    value = st.session_state[source_key]
    for key in all_keys:
        if key != source_key:
            st.session_state[key] = value


def demographic_selector(tab: str) -> str:
    validate_tab(tab)

    key = f"{tab}_demo_value"
    options = [
        "Foreign-born",
        "Percent Foreign-born",
        "Native",
        "Total",
    ]

    # When user updates any of these select boxes, update all other ones with the same value
    all_keys = [f"{one_tab}_demo_value" for one_tab in VALID_TABS]
    column = st.selectbox(
        "Demographic:",
        options=options,
        key=key,
        on_change=lambda: sync_values(key, all_keys),
    )
    return column


def location_selector(tab: str) -> str:
    validate_tab(tab)

    loc_key = f"{tab}_loc_value"
    all_loc_keys = [f"{one_tab}_loc_value" for one_tab in VALID_TABS]

    location_options = data.get_all_names()
    location = st.selectbox(
        "Location:",
        options=location_options,
        placeholder="Search for a place...",
        index=None,
        key=loc_key,
        on_change=lambda: sync_values(loc_key, all_loc_keys),
    )
    if location is None:
        location = "United States"
    return location


def location_and_demographic_block(tab: str) -> tuple[str, str, pd.DataFrame]:
    st.markdown(
        "**Start typing** the name of a State, County, or City to search for it. "
        "Or leave blank to view totals for the entire United States."
    )
    col1, col2 = st.columns(2)

    with col1:
        location = location_selector(tab)
        st.markdown("_(Tip: start typing to filter the list)_")

    with col2:
        column = demographic_selector(tab)

    df = data.get_data_for_name(location)
    return location, column, df


def state_selector(tab: str) -> str:
    validate_tab(tab)

    state_key = f"{tab}_state_value"
    all_keys = [f"{one_tab}_state_value" for one_tab in VALID_TABS]

    state_options = ["All States"] + data.get_all_states()
    state = st.selectbox(
        "State:",
        options=state_options,
        key=state_key,
        on_change=lambda: sync_values(state_key, all_keys),
    )

    return state
