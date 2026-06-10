import pandas as pd

from api.client import ZafronixClient

client = ZafronixClient()

def load_bracket(year):
    response = client.get(
        "bracket",
        {
            "year":year
        }
    )
    bracket_df = pd.json_normalize(response)

    bracket_df["tournament_year"] = year

    return bracket_df
