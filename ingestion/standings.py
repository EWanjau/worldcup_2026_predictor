import pandas as pd

from api.client import ZafronixClient

client = ZafronixClient()

def load_standings(year):
    response = client.get(
        "standings",
        {
            "year":year
        }
    )
    standings_df = pd.DataFrame(response)

    standings_df["tournament_year"] = year

    return standings_df
