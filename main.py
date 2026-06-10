from pathlib import Path

from ingestion.main_dataset_builder import main as build_raw_datasets


PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
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


def main():
    found_files, missing_files = check_raw_files()

    if found_files:
        print("\nData files found :")
        for filename in found_files:
            print(f"-> {filename}")

    if missing_files:
        print("Missing raw data files:")
        for filename in missing_files:
            print(f"- {RAW_DATA_DIR / filename}")

        print("Building raw datasets from the API...")
        build_raw_datasets()
        return

    print("All required raw data files found. Skipping ingestion API calls.\n")


if __name__ == "__main__":
    main()
