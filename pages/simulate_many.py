import streamlit as st
import pandas as pd

from src.streamlit_utils import load_predictor

predictor = load_predictor()

st.title(
    "📊 Monte Carlo Simulation"
)

runs = st.slider(
    "Simulations",
    100,
    10000,
    1000,
    step=100
)

if st.button(
    "Run"
):

    predictor.load_2026_teams()

    for group in predictor.groups:

        predictor.simulate_group(group)

    qualifiers = (
        predictor.get_group_qualifiers()
    )

    mc = predictor.run_many_simulations(
        qualifiers,
        n_simulations=runs
    )

    df = pd.DataFrame(
        mc["probabilities"]
    )

    st.dataframe(df)

    st.bar_chart(
        df.set_index("team")["probability"]
    )