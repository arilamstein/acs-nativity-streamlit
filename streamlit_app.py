import streamlit as st
import acs_nativity
import data_access as data

st.title("U.S. Foreign‑Born Population Trends")
st.markdown(
    """
    Explore how the foreign‑born and native‑born populations have changed 
    across the United States since 2005.  
    Choose a location to view its trends, and use **Zoom to** for county‑ or city‑level detail.
    """
)

# Let user select what data they want to see.
col1, col2, col3 = st.columns(3)
with col1:
    # View data for either the entire country or a state
    location_options = ["Nation"] + data.get_state_names()
    location = st.selectbox(label="Location:", options=location_options)
with col2:
    # When looking at a state, let user choose either the entire state or
    # a county or place within the state.
    # Disable when user is looking at entire nation
    disabled = location == "Nation"
    zoom_options = ["-"]
    if location != "Nation":
        zoom_options += sorted(
            data.get_county_names(location) + data.get_place_names(location)
        )
    zoom_to = st.selectbox(label="Zoom to:", options=zoom_options, disabled=disabled)
with col3:
    column = st.selectbox(
        "Demographic:",
        options=["Foreign-born", "Percent Foreign-born", "Native", "Total"],
    )

# Now get data
if location == "Nation":
    df = data.get_nation_data()
# Data for a state or sub-region of a state
elif location in data.get_state_names():
    if zoom_to == "-":  # data for an entire state
        df = data.get_state_data(location)
    elif zoom_to in data.get_county_names(location):  # data for a county in a state
        df = data.get_county_data(location, zoom_to)
    elif zoom_to in data.get_place_names(location):  # data for a place in a state
        df = data.get_place_data(location, zoom_to)
    else:
        raise ValueError("Unknown sub-region {zoom_to} for state {location}")
else:
    raise ValueError(f"Unknown State {location}")

# Make charts
tab1, tab2 = st.tabs(["📈 Trend", "📊 Year‑to‑Year Change"])
with tab1:
    st.plotly_chart(acs_nativity.plot_nativity_timeseries(df, column))

with tab2:
    st.plotly_chart(acs_nativity.plot_nativity_change(df, column))
