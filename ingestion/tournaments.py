import pandas as pd

from api.client import ZafronixClient

client = ZafronixClient()

def load_tournaments():
    response = client.get("tournaments")

    tournaments_df = pd.DataFrame(response)

    return tournaments_df

