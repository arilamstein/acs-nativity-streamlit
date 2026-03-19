from acs_nativity import get_nativity_timeseries
from censusdis import states
import pandas as pd


def get_us_data(end_year: int = 2024, verbose: bool = True) -> pd.DataFrame:
    if verbose:
        print("Generating US data")

    df_us = get_nativity_timeseries(end_year=end_year, us="*")

    # Sort by year so new data will always appear at the end,
    # which makes diffs easy to read.
    df_us = df_us.sort_values("Year")

    if verbose:
        print("Completed generating US data")

    return df_us


def get_state_data(end_year: int = 2024, verbose: bool = True) -> pd.DataFrame:
    if verbose:
        print("Generating state data")

    df_state = get_nativity_timeseries(end_year=end_year, state="*")
    df_state = df_state[df_state["Name"] != "Puerto Rico"]

    # Sort by year so new data will always appear at the end,
    # which makes diffs easy to read. Sorting by name just makes it deterministic.
    df_state = df_state.sort_values(["Year", "Name"])

    if verbose:
        print("Completed generating state data")

    return df_state


def get_county_data(end_year: int = 2024, verbose: bool = True) -> pd.DataFrame:
    if verbose:
        print("Generating county data")

    # API only lets you get all counties in a state, so we have to iterate over all states.
    dfs_county = []
    for state in states.ALL_STATES_AND_DC:
        if verbose:
            print(f"Getting data for {states.NAMES_FROM_IDS[state]}")
        df_new = get_nativity_timeseries(state=state, county="*")
        dfs_county.append(df_new)

    df_county = pd.concat(dfs_county)

    # Names come in like "Nassau county, New York" - use the comma to split into
    # separate State and County columns
    num_commas = df_county["Name"].str.count(",")
    if not (num_commas == 1).all():
        raise ValueError("Not all county names have exactly 1 comma!")
    df_county[["County", "State"]] = df_county["Name"].str.split(",", expand=True)
    df_county["County"] = df_county["County"].str.strip()
    df_county["State"] = df_county["State"].str.strip()
    # Reorder so state and county appear on the left
    df_county = df_county[
        [
            "State",
            "County",
            "Name",
            "Year",
            "Total",
            "Native",
            "Foreign-born",
            "Percent Foreign-born",
        ]
    ]

    # Sort by year so new data will always appear at the end,
    # which makes diffs easy to read. Sorting by state and county just makes it deterministic.
    df_county = df_county.sort_values(["Year", "State", "County"])

    if verbose:
        print("Completed generating county data")

    return df_county


def get_place_data(end_year: int = 2024, verbose: bool = True) -> pd.DataFrame:
    if verbose:
        print("Generating place data")

    # Census only includes data for places with population >=65k.
    # For at least for some years these states have had no data,
    # and this causes censusdis to throw a 204 error.
    # For now it's best to just skip these states.
    NO_DATA_STATES = [states.ME, states.VT, states.WV, states.WY]

    # Places can only be gotten at the state level.
    # So we need to iterate over all states
    dfs_place = []
    for state in states.ALL_STATES_AND_DC:
        if state in NO_DATA_STATES:
            if verbose:
                print(f"Skipping {states.NAMES_FROM_IDS[state]} due to low population")
            continue
        if verbose:
            print(f"Getting data for {states.NAMES_FROM_IDS[state]}")
        df_new = get_nativity_timeseries(state=state, place="*")
        dfs_place.append(df_new)

    df_place = pd.concat(dfs_place)

    # The name column is like "New York city, New York".
    # Split it into separate columns for place and state, and then put
    # that info first
    num_commas = df_place["Name"].str.count(",")
    if not (num_commas == 1).all():
        raise ValueError("Not all place names have exactly 1 comma!")
    df_place[["Place", "State"]] = df_place["Name"].str.split(",", expand=True)
    df_place["Place"] = df_place["Place"].str.strip()
    df_place["State"] = df_place["State"].str.strip()
    df_place = df_place[
        [
            "State",
            "Place",
            "Name",
            "Year",
            "Total",
            "Native",
            "Foreign-born",
            "Percent Foreign-born",
        ]
    ]

    # Sort by year so new data goes at the end.
    # Sorting by state and place makes it deterministic.
    df_place = df_place.sort_values(["Year", "State", "Place"])

    if verbose:
        print("Completed generating place data")

    return df_place
