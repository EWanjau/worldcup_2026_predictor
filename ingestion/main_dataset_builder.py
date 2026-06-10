from pathlib import Path

from .matches import build_matches_datasets
from .teams import build_teams_dataset
from .tournaments import load_tournaments


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main():
    tournaments_df = load_tournaments()

    matches_df = build_matches_datasets()

    teams_df = build_teams_dataset()

    print("=" * 50)
    print("Tournaments")
    print(tournaments_df.head())

    print("=" * 50)
    print("Teams")
    print(teams_df.head())

    print("=" * 50)
    print("Matches Type")
    print(matches_df.shape)

    print("=" * 50)
    print("Matches Info")
    print(matches_df.info())

    # 2. Save the dataframes into csv files
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    tournaments_df.to_csv(
        RAW_DATA_DIR / "tournaments.csv",
        index=False
    )

    matches_df.to_csv(
        RAW_DATA_DIR / "matches.csv",
        index=False
    )

    teams_df.to_csv(
        RAW_DATA_DIR / "teams.csv",
        index=False
    )


if __name__ == "__main__":
    main()
