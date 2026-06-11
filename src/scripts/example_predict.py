#!/usr/bin/env python
"""
Example script to run World Cup predictions and see results on terminal.
Run with: python src/scripts/example_predict.py
"""

import sys
import os
from pathlib import Path

# Add project root to path (go up from scripts/ -> src/ -> project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from src.worldcup_predictor import WorldCupPredictor

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def main():
    print_section("WORLD CUP 2026 PREDICTOR - EXAMPLE")

    # Step 1: Load data
    print("\n[1/9] Loading data files...")
    try:
        matches = pd.read_csv("data/raw/matches.csv")
        teams = pd.read_csv("data/raw/teams.csv")
        tournaments = pd.read_csv("data/raw/tournaments.csv")
        print(f"✓ Matches: {matches.shape[0]} records")
        print(f"✓ Teams: {teams.shape[0]} records")
        print(f"✓ Tournaments: {tournaments.shape[0]} records")
    except FileNotFoundError:
        print("✗ Error: Data files not found in data/raw/")
        print("  Run: python main.py prepare-data")
        return

    # Step 2: Initialize predictor
    print("\n[2/9] Initializing predictor...")
    predictor = WorldCupPredictor()
    predictor.load_data(matches, teams, tournaments)
    print("✓ Predictor initialized")

    # Step 3: Clean data
    print("\n[3/9] Cleaning data...")
    predictor.clean_data()
    predictor.remove_future_matches()
    predictor.standardize_team_names()
    predictor.validate_data()
    print("✓ Data cleaned and validated")

    # Step 4: Build features
    print("\n[4/9] Building features...")
    predictor.build_target()
    predictor.sort_matches()
    predictor.calculate_elo()
    print("  ✓ Elo ratings calculated")
    predictor.build_rolling_features()
    print("  ✓ Rolling form features built")
    predictor.build_head_to_head()
    print("  ✓ Head-to-head features built")
    predictor.build_historical_features()
    print("  ✓ Historical features built")
    predictor.build_stage_weight()
    print("  ✓ Stage weights created")

    # Step 5: Prepare training data
    print("\n[5/9] Preparing training data...")
    predictor.build_training_dataset()
    predictor.select_features()
    predictor.split_data()
    print(f"✓ Training set: {predictor.X_train.shape[0]} matches")
    print(f"✓ Test set: {predictor.X_test.shape[0]} matches")

    # Step 6: Train model
    print("\n[6/9] Training CatBoost model...")
    print("(This may take 1-3 minutes)")
    predictor.train_model(iterations=200)  # Reduced for faster demo
    print("✓ Model training completed")

    # Step 7: Evaluate model
    print("\n[7/9] Evaluating model...")
    results = predictor.evaluate_model()
    print("✓ Model evaluated")

    # Step 8: Show feature importance
    print("\n[8/9] Feature importance analysis...")
    importance_df = predictor.feature_importance()
    print("\nTop 10 most important features:")
    for idx, row in importance_df.head(10).iterrows():
        bar = "█" * int(row['importance'] / 2)
        print(f"  {idx+1:2d}. {row['feature']:30s} {bar} {row['importance']:.2f}")

    # Step 9: Make predictions
    print_section("MATCH PREDICTIONS")

    # List of interesting matchups
    matchups = [
        ("Brazil", "Germany"),
        ("France", "Argentina"),
        ("England", "Spain"),
        ("Belgium", "Netherlands"),
    ]

    print("\nPredicting match outcomes:\n")

    for team_a, team_b in matchups:
        # Get prediction
        pred = predictor.predict_match(team_a, team_b, stage_weight=5)

        # Get probabilities
        proba = predictor.predict_match_proba(team_a, team_b, stage_weight=5)

        print(f"{team_a:20s} vs {team_b:20s}")
        print(f"  Prediction: {pred['result']}")
        print(f"  Probabilities:")
        print(f"    • {team_a:20s} Win: {proba['team_a_win']:6.2%}")
        print(f"    • Draw:                {proba['draw']:6.2%}")
        print(f"    • {team_b:20s} Win: {proba['team_b_win']:6.2%}")
        print()

    # Tournament simulation
    print_section("TOURNAMENT SIMULATION")

    print("\nLoading 2026 World Cup groups...")
    predictor.load_2026_teams()
    print(f"✓ Loaded {len(predictor.groups)} groups with {sum(len(teams) for teams in predictor.groups.values())} teams")

    print("\nSimulating group stage matches...")
    for group in predictor.groups:
        predictor.simulate_group(group)
    print("✓ Group stage simulated")

    print("\nDetermining qualifiers...")
    qualifiers = predictor.get_group_qualifiers()
    print(f"✓ {len(qualifiers['qualified'])} teams qualified for knockout stage")

    print("\nRunning 1000 Monte Carlo tournament simulations...")
    print("(This simulates the entire tournament 1000 times to estimate probabilities)")
    mc_results = predictor.run_many_simulations(qualifiers, n_simulations=1000)
    print("✓ Simulations completed")

    # Display championship probabilities
    print_section("CHAMPIONSHIP PROBABILITIES")

    probs = mc_results['probabilities']
    print("\nTop 20 teams by championship probability:\n")

    for i, team_prob in enumerate(probs[:20], 1):
        percentage = team_prob['probability']
        wins = team_prob['wins']
        bar_width = int(percentage / 2)
        bar = "█" * bar_width

        print(f"{i:2d}. {team_prob['team']:25s} {percentage:6.2f}%  {bar}  ({wins:,} wins)")

    print("\n" + "="*70)
    print("Summary Statistics:")
    print("="*70)

    top_3_prob = sum(p['probability'] for p in probs[:3])
    top_10_prob = sum(p['probability'] for p in probs[:10])

    print(f"Top 3 teams probability:   {top_3_prob:.2f}%")
    print(f"Top 10 teams probability:  {top_10_prob:.2f}%")
    print(f"Champion (most likely):    {probs[0]['team']} ({probs[0]['probability']:.2f}%)")

    print_section("COMPLETE")
    print("\n✓ All predictions and simulations completed!")
    print(f"\nModel saved to: models/worldcup_predictor/")
    print(f"Training tournaments: {predictor.train_years}")
    print(f"Testing tournaments:  {predictor.test_years}")

    # Optionally plot
    try:
        print("\nGenerating visualization...")
        predictor.plot_probabilities(mc_results, top_n=10)
        print("✓ Plot displayed")
    except Exception as e:
        print(f"⚠ Could not display plot: {e}")

if __name__ == "__main__":
    main()
