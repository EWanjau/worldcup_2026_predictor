import pandas as pd

from api.client import ZafronixClient
from .tournaments import load_tournaments

client = ZafronixClient()

# 1. Load matches by specified year

def load_matches(year):
    response = client.get(
        "matches",{
            "year":year
        }
    )
    matches_df = pd.DataFrame(response["data"])
    matches_df["tournament_year"] = year

    return matches_df

# 2. Load all Historical matches for all teams

def build_matches_datasets():
    tournaments_df = load_tournaments()

    matches =[]

    for year in tournaments_df["year"]:
        print(f"Downloading {year}")

        df = load_matches(year)

        matches.append(df)

    matches_df = pd.concat(
        matches,
        ignore_index=True
    )
    return matches_df
