from acs_nativity import get_nativity_timeseries
from censusdis import states
import pandas as pd
import time

start = time.time()

END_YEAR = 2024

# National data
print("Generating US data")
us_filename = "us.csv"

df_us = get_nativity_timeseries(end_year=END_YEAR, us="*")

df_us = df_us.sort_values("Year")
df_us.to_csv(us_filename, index=False)
print(f"US data written to {us_filename}!")

# State data
print("Generating state data")
state_filename = "state.csv"

df_state = get_nativity_timeseries(end_year=END_YEAR, state="*")
df_state = df_state[df_state["Name"] != "Puerto Rico"]

df_state = df_state.sort_values(["Year", "Name"])
df_state.to_csv(state_filename, index=False)
print(f"State data generated to {state_filename}!")

# County data
print("Generating county data")
county_filename = "county.csv"

dfs_county = []
for state in states.ALL_STATES_AND_DC:
    print(f"Getting data for {states.NAMES_FROM_IDS[state]}")
    df_new = get_nativity_timeseries(state=state, county="*")
    dfs_county.append(df_new)

df_county = pd.concat(dfs_county)

# Split Name column into two columns
num_commas = df_county["Name"].str.count(",")
if not (num_commas == 1).all():
    raise ValueError("Not all county names have exactly 1 comma!")
df_county[["County", "State"]] = df_county["Name"].str.split(",", expand=True)
df_county["County"] = df_county["County"].str.strip()
df_county["State"] = df_county["State"].str.strip()
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

df_county = df_county.sort_values(["Year", "State", "County"])
df_county.to_csv(county_filename, index=False)
print(f"County data generated to {county_filename}!")

# Place data
print("Generating place data")
place_filename = "place.csv"

# Census only includes data for places with population >=65k.
# For at least for some years these states have had no data,
# and this causes censusdis to throw a 204 error.
# For now it's best to just skip these states.
NO_DATA_STATES = [states.ME, states.VT, states.WV, states.WY]

dfs_place = []
for state in states.ALL_STATES_AND_DC:
    if state in NO_DATA_STATES:
        print(f"Skipping {states.NAMES_FROM_IDS[state]} due to low population")
        continue
    print(f"Getting data for {states.NAMES_FROM_IDS[state]}")
    df_new = get_nativity_timeseries(state=state, place="*")
    dfs_place.append(df_new)

df_place = pd.concat(dfs_place)

# Split Name column into two columns
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

df_place = df_place.sort_values(["Year", "State", "Place"])
df_place.to_csv(place_filename, index=False)
print(f"Place data generated to {place_filename}!")


def format_duration(seconds: float) -> str:
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)

    if hours > 0:
        return f"{hours}h {minutes}m {sec}s"
    elif minutes > 0:
        return f"{minutes}m {sec}s"
    else:
        return f"{sec}s"


end = time.time()
duration = end - start

print(f"Ran in {format_duration(duration)}")
