from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ingestion.main_dataset_builder import main as build_raw_datasets
from src.worldcup_predictor import WorldCupPredictor


PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_MODEL_DIR = PROJECT_ROOT / "models" / "worldcup_predictor"
REQUIRED_RAW_FILES = (
    "matches.csv",
    "teams.csv",
    "tournaments.csv",
)


def check_raw_files():
    found_files = []
    missing_files = []

    for filename in REQUIRED_RAW_FILES:
        if (RAW_DATA_DIR / filename).is_file():
            found_files.append(filename)
        else:
            missing_files.append(filename)

    return found_files, missing_files


def ensure_raw_data():
    found_files, missing_files = check_raw_files()

    if found_files:
        print("\nData files found:")
        for filename in found_files:
            print(f"-> {filename}")

    if missing_files:
        print("Missing raw data files:")
        for filename in missing_files:
            print(f"- {RAW_DATA_DIR / filename}")

        print("Building raw datasets from the API...")
        build_raw_datasets()
        return False

    print("All required raw data files found. Skipping ingestion API calls.\n")
    return True


def load_raw_data(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    matches = pd.read_csv(raw_dir / "matches.csv")
    teams = pd.read_csv(raw_dir / "teams.csv")
    tournaments = pd.read_csv(raw_dir / "tournaments.csv")
    return matches, teams, tournaments


def run_training(raw_dir: Path, model_dir: Path) -> WorldCupPredictor:
    matches, teams, tournaments = load_raw_data(raw_dir)

    predictor = WorldCupPredictor()
    predictor.load_data(matches, teams, tournaments)
    predictor.clean_data()
    predictor.remove_future_matches()
    predictor.standardize_team_names()
    predictor.validate_data()
    predictor.build_target()
    predictor.sort_matches()
    predictor.calculate_elo()
    predictor.build_rolling_features()
    predictor.build_head_to_head()
    predictor.build_historical_features()
    predictor.build_stage_weight()
    predictor.build_training_dataset()
    predictor.select_features()
    predictor.split_data()
    predictor.train_model()
    predictor.evaluate_model()
    predictor.feature_importance()
    predictor.save_model(str(model_dir))

    return predictor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="worldcup-predictor",
        description="World Cup predictor project entry point.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "prepare-data",
        help="Check for raw CSVs and build them from the API if they are missing.",
    )

    train = subparsers.add_parser(
        "train",
        help="Run the full training pipeline and export model artifacts.",
    )
    train.add_argument(
        "--raw-dir",
        type=Path,
        default=RAW_DATA_DIR,
        help="Directory containing matches.csv, teams.csv, and tournaments.csv",
    )
    train.add_argument(
        "--model-dir",
        type=Path,
        default=DEFAULT_MODEL_DIR,
        help="Directory where model artifacts will be saved",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "train":
        run_training(args.raw_dir, args.model_dir)
        return

    ensure_raw_data()


if __name__ == "__main__":
    main()
