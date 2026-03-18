import streamlit as st
import pandas as pd
import acs_nativity

# Load all data
df_us = pd.read_csv("us.csv")
df_state = pd.read_csv("state.csv")
df_county = pd.read_csv("county.csv")

# Let use choose what to see
geography = st.selectbox(label="Geography:", options=["Nation", "State", "County"])
if geography == "Nation":
    df = df_us
elif geography == "State":
    df = df_state.copy()
    state = st.selectbox(label="State:", options=df["Name"].unique())
    df = df[df["Name"] == state]

elif geography == "County":
    df = df_county.copy()
    state = st.selectbox(label="State:", options=df["State"].unique())
    counties = df[df["State"] == state]["County"]
    county = st.selectbox(label="County:", options=counties.unique())
    df = df[(df["State"] == state) & (df["County"] == county)]
else:
    raise ValueError("Unknown geography")

column = st.selectbox(
    "Demographic:", options=["Foreign-born", "Percent Foreign-born", "Native", "Total"]
)

# Make charts
st.plotly_chart(acs_nativity.plot_nativity_timeseries(df, column))
st.plotly_chart(acs_nativity.plot_nativity_change(df, column))
