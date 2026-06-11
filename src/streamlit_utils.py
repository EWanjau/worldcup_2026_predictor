import streamlit as st
from pathlib import Path

from src.worldcup_predictor import WorldCupPredictor


@st.cache_resource
def load_predictor():

    predictor = WorldCupPredictor()

    # Load trained model
    predictor.load_saved_model()

    # Base directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load datasets needed for feature generation
    predictor.load_data(
        BASE_DIR / "data/raw/matches.csv",
        BASE_DIR / "data/raw/teams.csv",
        BASE_DIR / "data/raw/tournaments.csv"
    )

    predictor.clean_data()

    predictor.standardize_team_names()

    # Load 2026 groups
    predictor.load_2026_teams()

    return predictor