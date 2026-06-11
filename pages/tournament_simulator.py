import streamlit as st

from src.streamlit_utils import load_predictor

predictor = load_predictor()

st.title(
    "🏆 Tournament Simulator"
)

if st.button(
    "Simulate Tournament"
):

    predictor.load_2026_teams()

    for group in predictor.groups:

        predictor.simulate_group(group)

    qualifiers = (
        predictor.get_group_qualifiers()
    )

    result = (
        predictor.simulate_tournament(
            qualifiers
        )
    )

    st.success(
        f'Champion: {result["champion"]}'
    )