from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

df_nation = pd.read_csv(DATA_DIR / "us.csv")
df_state = pd.read_csv(DATA_DIR / "state.csv")
df_county = pd.read_csv(DATA_DIR / "county.csv")
df_place = pd.read_csv(DATA_DIR / "place.csv")


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


def get_place_names(state: str) -> list[str]:
    return df_place[df_place["State"] == state]["Place"].unique().tolist()


def get_place_data(state: str, place: str) -> pd.DataFrame:
    return df_place[(df_place["State"] == state) & (df_place["Place"] == place)].copy()
