from pathlib import Path
import pandas as pd
from pandas.io.formats.style import Styler

DATA_DIR = Path("data")
df_all = pd.concat(
    [
        pd.read_csv(DATA_DIR / "us.csv"),
        pd.read_csv(DATA_DIR / "state.csv"),
        pd.read_csv(DATA_DIR / "county.csv"),
        pd.read_csv(DATA_DIR / "place.csv"),
    ]
)
# Certain cities (especially "unincoporated cities" in Virginia) appear twice in the
# underlying data - once in the county file and once in the place data.
df_all = df_all.drop_duplicates(subset=["Name", "Year"]).reset_index(drop=True)


def get_all_states() -> list[str]:
    return sorted(df_all["State"].dropna().unique().tolist())


def get_all_names() -> list[str]:
    return sorted(df_all["Name"].unique().tolist())


def get_data_for_name(name: str) -> pd.DataFrame:
    return df_all[df_all["Name"] == name].copy().sort_values("Year")


def style_nativity_table(df: pd.DataFrame) -> Styler:
    fmt = {
        "Total": lambda x: f"{x:,.0f}",
        "Native": lambda x: f"{x:,.0f}",
        "Foreign-born": lambda x: f"{x:,.0f}",
        "Percent Foreign-born": lambda x: f"{x:.1f}%",
    }
    return df.style.format(fmt)  # type: ignore[arg-type]


def get_table_df(state: str, latest_only: bool) -> pd.DataFrame:
    df = df_all.copy()

    # Optionally subset to the latest year
    if latest_only:
        max_year = df["Year"].max()
        df = df[df["Year"] == max_year]

    if state != "All States":
        df = df[df["State"] == state]

    # Drop columns I added to support zoom
    df = df.drop(columns=["State", "County", "Place"], errors="ignore")
    df = df.sort_values("Percent Foreign-born", ascending=False)

    return df


def get_table_df_styled(state: str, latest_only: bool) -> Styler:
    df = get_table_df(state, latest_only)
    return style_nativity_table(df)


def get_years() -> list[int]:
    return sorted(df_all["Year"].unique().tolist())


def get_compare_df(state: str, year1: int, year2: int, column: str) -> pd.DataFrame:
    """
    Return a wide DataFrame with Name, year1, year2, and change columns
    for the given location and column.
    """
    # Pivot so we can easily compare years
    df = get_table_df(state, False)
    df_wide = df.pivot(index="Name", columns="Year", values=column).reset_index()
    df_wide.columns.name = None

    # Years are ints, and "mixed type" columns generates a warning,
    # so convert all columns to string.
    # Also convert the incoming year variables to strings for consistency
    df_wide.columns = df_wide.columns.map(str)
    y1 = str(year1)
    y2 = str(year2)

    # Compute change
    df_wide = df_wide[["Name", y1, y2]].dropna()
    df_wide["Change"] = df_wide[y2] - df_wide[y1]

    if column == "Percent Foreign-born":
        # If we're comparing percents, rename "Change" column to "Change (pct points)"
        # for clarity and sort on it
        df_wide = df_wide.rename(columns={"Change": "Change (pct points)"})
        df_wide = df_wide.sort_values("Change (pct points)", ascending=False)
    else:
        # Otherwise add a "Percent Change" column and sort on it
        df_wide["Percent Change"] = df_wide["Change"] / df_wide[y1] * 100
        df_wide = df_wide.sort_values("Percent Change", ascending=False)

    return df_wide


def style_compare_table(
    df: pd.DataFrame, year1: int, year2: int, column: str
) -> Styler:
    # If we are comparing percentages, then add a % to the year columns
    # but not the compare column.
    if column == "Percent Foreign-born":
        fmt = {
            str(year1): lambda x: f"{x:.1f}%",
            str(year2): lambda x: f"{x:.1f}%",
            "Change (pct points)": lambda x: f"{x:.1f}",
        }
    # Otherwise just add a % to the "Percent Change" column.
    else:
        fmt = {
            str(year1): lambda x: f"{x:,.0f}",
            str(year2): lambda x: f"{x:,.0f}",
            "Change": lambda x: f"{x:,.0f}",
            "Percent Change": lambda x: f"{x:,.1f}%",
        }
    return df.style.format(fmt)  # type: ignore[arg-type]


def get_compare_df_styled(state: str, year1: int, year2: int, column: str) -> Styler:
    df = get_compare_df(state, year1, year2, column)
    return style_compare_table(df, year1, year2, column)
