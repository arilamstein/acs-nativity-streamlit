import streamlit as st
import data_access as data

VALID_TABS = ["bar", "line", "table", "compare"]


def validate_tab(tab: str) -> None:
    if tab not in VALID_TABS:
        raise ValueError(f"tab must one of {VALID_TABS}. {tab} given")


def gen_key(tab: str, ui_element: str) -> str:
    return f"{tab}_{ui_element}"


def update_keys(updated_key: str) -> None:
    new_value = st.session_state[updated_key]

    ui_element = updated_key.partition("_")[2]
    for one_tab in VALID_TABS:
        key_to_update = gen_key(one_tab, ui_element)
        if key_to_update != updated_key:
            st.session_state[key_to_update] = new_value


def demographic_selector(tab: str) -> str:
    validate_tab(tab)

    options = [
        "Foreign-born",
        "Percent Foreign-born",
        "Native",
        "Total",
    ]

    key = gen_key(tab, "demographic_selector")
    column = st.selectbox(
        "Demographic:",
        options=options,
        key=key,
        on_change=lambda: update_keys(key),
    )
    return column


def location_selector(tab: str) -> str:
    validate_tab(tab)

    location_options = data.get_all_names()
    key = gen_key(tab, "location_selector")
    location = st.selectbox(
        "Location:",
        options=location_options,
        placeholder="Search for a place...",
        index=None,
        key=key,
        on_change=lambda: update_keys(key),
    )
    if location is None:
        location = "United States"
    return location


def location_and_demographic_block(tab: str) -> tuple[str, str]:
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

    return location, column


def state_selector(tab: str) -> str:
    validate_tab(tab)

    state_options = ["All States"] + data.get_all_states()
    key = gen_key(tab, "state_selector")
    state = st.selectbox(
        "State:",
        options=state_options,
        key=key,
        on_change=lambda: update_keys(key),
    )

    return state
