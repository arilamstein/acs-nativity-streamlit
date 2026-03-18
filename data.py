import pandas as pd

df_nation = pd.read_csv("us.csv")
df_state = pd.read_csv("state.csv")
df_county = pd.read_csv("county.csv")


def get_nation_data() -> pd.DataFrame:
    return df_nation.copy()


def get_state_names() -> list[str]:
    return df_state["Name"].unique().tolist()


def get_state_data(state: str) -> pd.DataFrame:
    return df_state[df_state["Name"] == state].copy()


def get_county_names(state: str) -> list[str]:
    return df_county[df_county["State"] == state]["County"].unique().tolist()


def get_county_data(state: str, county: str) -> pd.DataFrame:
    return df_county[
        (df_county["State"] == state) & (df_county["County"] == county)
    ].copy()
