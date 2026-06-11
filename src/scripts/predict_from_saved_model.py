#!/usr/bin/env python
"""
Load the saved trained model and make predictions WITHOUT retraining.
Run with: python src/scripts/predict_from_saved_model.py
"""

import pickle
import json
import pandas as pd
from catboost import CatBoostClassifier
from pathlib import Path

# Set up paths (go up from scripts/ -> src/ -> project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "models" / "worldcup_predictor"

print("\n" + "="*70)
print("  LOADING SAVED MODEL FOR PREDICTIONS")
print("="*70)

# Step 1: Load model artifacts
print("\n[1/4] Loading model artifacts...")

try:
    # Load the CatBoost model
    model = CatBoostClassifier()
    model.load_model(str(MODEL_DIR / "catboost_model.cbm"))
    print("  ✓ CatBoost model loaded")

    # Load feature columns
    with open(MODEL_DIR / "feature_columns.pkl", "rb") as f:
        feature_columns = pickle.load(f)
    print("  ✓ Feature columns loaded")

    # Load class labels
    with open(MODEL_DIR / "class_labels.pkl", "rb") as f:
        class_labels = pickle.load(f)
    print("  ✓ Class labels loaded")

    # Load team history (for rolling features)
    with open(MODEL_DIR / "team_history.pkl", "rb") as f:
        team_history = pickle.load(f)
    print("  ✓ Team history loaded")

    # Load head-to-head history
    with open(MODEL_DIR / "h2h_history.pkl", "rb") as f:
        h2h_history = pickle.load(f)
    print("  ✓ Head-to-head history loaded")

    # Load current Elo ratings
    with open(MODEL_DIR / "current_elo.pkl", "rb") as f:
        current_elo = pickle.load(f)
    print("  ✓ Current Elo ratings loaded")

    # Load metadata
    with open(MODEL_DIR / "metadata.json", "r") as f:
        metadata = json.load(f)
    print("  ✓ Metadata loaded")

except Exception as e:
    print(f"  ✗ Error loading model: {e}")
    exit(1)

# Step 2: Display model information
print("\n[2/4] Model Information")
print(f"  Training tournaments: {metadata['train_years']}")
print(f"  Testing tournaments: {metadata['test_years']}")
print(f"  Number of features: {metadata['n_features']}")
print(f"  Model type: {metadata['model_type']}")
print(f"  Target classes: {metadata['target_mapping']}")

# Step 3: Create prediction function
print("\n[3/4] Setting up prediction functions...")

def get_team_snapshot(team_name):
    """Get the latest snapshot for a team."""
    elo = current_elo.get(team_name, 1500)

    matches = team_history.get(team_name, [])
    recent = matches[-5:]

    if len(recent) == 0:
        win_rate = 0.5
        goals = 1.0
        conceded = 1.0
        goal_diff = 0.0
    else:
        win_rate = sum(x["result"] for x in recent) / len(recent)
        goals = sum(x["gf"] for x in recent) / len(recent)
        conceded = sum(x["ga"] for x in recent) / len(recent)
        goal_diff = goals - conceded

    snapshot = {
        "elo": elo,
        "win_rate_last_5": win_rate,
        "goals_last_5": goals,
        "conceded_last_5": conceded,
        "goal_diff_last_5": goal_diff,
    }
    return snapshot


def build_match_features(team_a, team_b, stage_weight=1):
    """Build features for a match prediction."""
    home = get_team_snapshot(team_a)
    away = get_team_snapshot(team_b)

    pair = tuple(sorted([team_a, team_b]))
    h2h_matches = h2h_history.get(pair, [])

    if len(h2h_matches) == 0:
        h2h_games = 0
        h2h_win_rate = 0.5
        h2h_goal_diff = 0.0
    else:
        h2h_games = len(h2h_matches)
        h2h_win_rate = sum(x["result"] for x in h2h_matches) / h2h_games
        h2h_goal_diff = sum(x["goal_diff"] for x in h2h_matches) / h2h_games

    row = {
        "home_team_elo": home["elo"],
        "away_team_elo": away["elo"],
        "elo_difference": home["elo"] - away["elo"],
        "home_win_rate_last_5": home["win_rate_last_5"],
        "away_win_rate_last_5": away["win_rate_last_5"],
        "home_goals_last_5": home["goals_last_5"],
        "away_goals_last_5": away["goals_last_5"],
        "home_conceded_last_5": home["conceded_last_5"],
        "away_conceded_last_5": away["conceded_last_5"],
        "home_goal_diff_last_5": home["goal_diff_last_5"],
        "away_goal_diff_last_5": away["goal_diff_last_5"],
        "head_to_head_games": h2h_games,
        "head_to_head_win_rate": h2h_win_rate,
        "head_to_head_goal_difference": h2h_goal_diff,
        # For simplicity, set historical features to 0 (they won't change)
        "home_historical_titles": 0,
        "away_historical_titles": 0,
        "home_knockout_rate": 0,
        "away_knockout_rate": 0,
        "home_average_finish": 32,
        "away_average_finish": 32,
        "home_world_cup_appearances": 0,
        "away_world_cup_appearances": 0,
        "home_semi_final_rate": 0,
        "away_semi_final_rate": 0,
        "home_final_rate": 0,
        "away_final_rate": 0,
        "stage_weight": stage_weight,
    }

    features = pd.DataFrame([row])
    features = features[feature_columns]

    return features


def predict_match(team_a, team_b, stage_weight=1):
    """Predict a match outcome."""
    features = build_match_features(team_a, team_b, stage_weight)
    prediction = model.predict(features)
    prediction = prediction.flatten()[0]

    if prediction == 1:
        result = f"{team_a} Win"
    elif prediction == -1:
        result = f"{team_b} Win"
    else:
        result = "Draw"

    return {
        "team_a": team_a,
        "team_b": team_b,
        "prediction": int(prediction),
        "result": result,
    }


def predict_match_proba(team_a, team_b, stage_weight=1):
    """Predict match probabilities."""
    features = build_match_features(team_a, team_b, stage_weight)
    probabilities = model.predict_proba(features)[0]

    output = {
        "team_a": team_a,
        "team_b": team_b,
        "probabilities": {},
    }

    for label, probability in zip(class_labels, probabilities):
        output["probabilities"][int(label)] = float(probability)

    output["team_a_win"] = output["probabilities"].get(1, 0.0)
    output["draw"] = output["probabilities"].get(0, 0.0)
    output["team_b_win"] = output["probabilities"].get(-1, 0.0)

    return output


print("  ✓ Prediction functions ready")

# Step 4: Make predictions
print("\n[4/4] Making Predictions")
print("="*70)

# List of interesting matchups
matchups = [
    ("Brazil", "Germany"),
    ("France", "Argentina"),
    ("England", "Spain"),
    ("Belgium", "Netherlands"),
]

print("\nPredicting match outcomes:\n")

for team_a, team_b in matchups:
    pred = predict_match(team_a, team_b, stage_weight=5)
    proba = predict_match_proba(team_a, team_b, stage_weight=5)

    print(f"{team_a:20s} vs {team_b:20s}")
    print(f"  Prediction: {pred['result']}")
    print(f"  Probabilities:")
    print(f"    • {team_a:20s} Win: {proba['team_a_win']:6.2%}")
    print(f"    • Draw:                {proba['draw']:6.2%}")
    print(f"    • {team_b:20s} Win: {proba['team_b_win']:6.2%}")
    print()

print("="*70)
print("✓ Predictions completed!")
print("="*70)

print("\n📌 USAGE:")
print("\nYou can now use these functions in your code:")
print("""
  from predict_from_saved_model import predict_match, predict_match_proba

  # Get a single prediction
  result = predict_match("France", "Brazil")
  print(result)  # {'team_a': 'France', 'team_b': 'Brazil', 'prediction': 1, 'result': 'France Win'}

  # Get probabilities
  proba = predict_match_proba("France", "Brazil", stage_weight=5)
  print(f"France win: {proba['team_a_win']:.2%}")
  print(f"Draw: {proba['draw']:.2%}")
  print(f"Brazil win: {proba['team_b_win']:.2%}")
""")

print("\n💡 TIP:")
print("  To use in other scripts, import the functions:")
print("  from predict_from_saved_model import predict_match, predict_match_proba\n")
