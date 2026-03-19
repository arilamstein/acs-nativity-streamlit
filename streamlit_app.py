import streamlit as st
import acs_nativity
import data

# Let use choose what to see
geography = st.selectbox(
    label="Geography:", options=["Nation", "State", "County", "Place"]
)
if geography == "Nation":
    df = data.get_nation_data()
elif geography == "State":
    state = st.selectbox(label="State:", options=data.get_state_names())
    df = data.get_state_data(state)
elif geography == "County":
    state = st.selectbox(label="State:", options=data.get_state_names())
    county = st.selectbox(label="County:", options=data.get_county_names(state))
    df = data.get_county_data(state, county)
elif geography == "Place":
    state = st.selectbox(label="State:", options=data.get_state_names())
    place = st.selectbox(label="Place:", options=data.get_place_names(state))
    df = data.get_place_data(state, place)
else:
    raise ValueError("Unknown geography")

column = st.selectbox(
    "Demographic:", options=["Foreign-born", "Percent Foreign-born", "Native", "Total"]
)

# Make charts
st.plotly_chart(acs_nativity.plot_nativity_timeseries(df, column))
st.plotly_chart(acs_nativity.plot_nativity_change(df, column))
