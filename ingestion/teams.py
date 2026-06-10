import pandas as pd
from api.client import ZafronixClient
from .tournaments import load_tournaments

client = ZafronixClient()

# 1. Extract Teams in each tournament

def load_tournament_teams(year):
    response = client.get(
        "teams",
        {
            "tournament":year
        }
    )
    teams_df = pd.DataFrame(response)
    teams_df["tournament_year"] = year

    return teams_df


# 1. Get each team history for every Tournament
def load_team(team_name):
    response = client.get(
        f"teams/{team_name}"
    )
    team_df = pd.json_normalize(response)

    return team_df

# 2. Build Team Datasets
def build_teams_dataset():
    tournaments_df = load_tournaments()
    teams = []
    for year in tournaments_df["year"]:
        df = load_tournament_teams(year)
        teams.append(df)

    teams_df = pd.concat(
        teams,
        ignore_index=True
    )
    teams_df = teams_df.drop_duplicates(
        subset=["name", "code", "iso", "tournament_year"]
    )
    return teams_df
