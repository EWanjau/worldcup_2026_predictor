import streamlit as st

from src.streamlit_utils import load_predictor

predictor = load_predictor()

st.title("⚽ Match Predictor")

teams = sorted(predictor.current_elo.keys())

team_a = st.selectbox("Team A", teams)
team_b = st.selectbox("Team B", teams)

if st.button("Predict"):
    result = predictor.predict_match_proba(team_a, team_b)
    st.write(result)