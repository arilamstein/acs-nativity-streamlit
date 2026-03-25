from pathlib import Path
import pandas as pd
from pandas.io.formats.style import Styler

DATA_DIR = Path("data")

df_us = pd.read_csv(DATA_DIR / "us.csv")
df_state = pd.read_csv(DATA_DIR / "state.csv")
df_county = pd.read_csv(DATA_DIR / "county.csv")
df_place = pd.read_csv(DATA_DIR / "place.csv")


def get_us_data() -> pd.DataFrame:
    return df_us.copy()


def get_state_names() -> list[str]:
    return df_state["Name"].unique().tolist()


def get_state_data(state: str) -> pd.DataFrame:
    return df_state[df_state["Name"] == state].copy()


def get_county_names(state: str) -> list[str]:
    return df_county[df_county["State"] == state]["County"].unique().tolist()


def get_county_data(state: str, county: str | None) -> pd.DataFrame:
    if county is None:  # Return all counties in the state
        return df_county[df_county["State"] == state].copy()
    else:
        return df_county[
            (df_county["State"] == state) & (df_county["County"] == county)
        ].copy()


def get_place_names(state: str) -> list[str]:
    return df_place[df_place["State"] == state]["Place"].unique().tolist()


def get_place_data(state: str, place: str | None) -> pd.DataFrame:
    if place is None:  # Return all places in the state
        return df_place[df_place["State"] == state].copy()
    else:
        return df_place[
            (df_place["State"] == state) & (df_place["Place"] == place)
        ].copy()


def style_nativity_table(df: pd.DataFrame) -> Styler:
    fmt = {
        "Total": lambda x: f"{x:,.0f}",
        "Native": lambda x: f"{x:,.0f}",
        "Foreign-born": lambda x: f"{x:,.0f}",
        "Percent Foreign-born": lambda x: f"{x:.1f}%",
    }
    return df.style.format(fmt)  # type: ignore[arg-type]


def get_all_data(
    location: str, latest_only: bool, style: bool
) -> pd.DataFrame | Styler:
    # For "United States" view, just return all data
    if location == "United States":
        df = pd.concat([df_us, df_state, df_county, df_place], ignore_index=True)
    # Otherwise just show data for a particular state.
    # That means: all state data, all county data, all place data - but only
    # for the selected state.
    else:
        df = pd.concat(
            [
                get_state_data(location),
                get_county_data(location, county=None),
                get_place_data(location, place=None),
            ],
            ignore_index=True,
        )

    # Optionally subset to the latest year
    if latest_only:
        max_year = df["Year"].max()
        df = df[df["Year"] == max_year]

    # Drop columns I added to support zoom
    df = df.drop(columns=["State", "County", "Place"], errors="ignore")
    df = df.sort_values("Percent Foreign-born", ascending=False)

    if style:
        return style_nativity_table(df)
    else:
        return df
