import streamlit as st
import pandas as pd
import acs_nativity

df_us = pd.read_csv("us.csv")
df_state = pd.read_csv("state.csv")
df_county = pd.read_csv("county.csv")

geography = st.selectbox(label="Geography:", options=["Nation", "State", "County"])
column = st.selectbox(
    "Demographic:", options=["Foreign-born", "Percent Foreign-born", "Native", "Total"]
)

st.plotly_chart(acs_nativity.plot_nativity_timeseries(df_us, column))
st.plotly_chart(acs_nativity.plot_nativity_change(df_us, column))
