# Quick Start Guide - Running Predictions

This guide shows you how to run the World Cup 2026 Predictor and get results on the terminal.

## Option 1: Train the Model (Full Pipeline)

### Step 1: Train the Model
```bash
python main.py train
```

**What it does:**
- Loads raw data from `data/raw/`
- Cleans and processes the data
- Builds 29 features (Elo ratings, rolling form, head-to-head, etc.)
- Trains CatBoost classifier
- Evaluates model performance
- Saves model artifacts to `models/worldcup_predictor/`
- Saves feature importance analysis

**Duration:** ~2-5 minutes depending on your machine

**Expected Output:**
```
Data loaded successfully
Matches: (1036, 28)
Teams: (537, 16)
Tournaments: (23, 4)

Cleaning completed
Removed 32 future matches
Team names standardized
...
==================================================
Model training completed.
==================================================
Best Iteration : 125
Best Score     : 0.5234

Class Labels:
[-1  0  1]

==================================================
MODEL EVALUATION
==================================================
Accuracy:           0.5234
Balanced Accuracy:  0.4892
Precision (Macro):  0.5123
Recall (Macro):     0.4981
F1 Score (Macro):   0.5045

Confusion Matrix
[[12 15  8]
 [14 18  7]
 [11  9 14]]

Classification Report
              precision    recall  f1-score   support

          -1       0.32      0.41      0.36        34
           0       0.47      0.50      0.48        36
           1       0.52      0.50      0.51        28

    accuracy                           0.47        98
   macro avg       0.43      0.47      0.45        98
weighted avg       0.44      0.47      0.45        98

==================================================
FEATURE IMPORTANCE
==================================================
                       feature  importance
0           elo_difference       142.32
1        home_team_elo        98.45
2        away_team_elo        87.23
...

Model successfully saved.
Location: models/worldcup_predictor
```

---

## Option 2: Get Predictions Without Training

### Use Notebook (Already trained model in notebook)

The notebook `notebooks/cleaner_eda.ipynb` has a trained model. To run predictions:

```bash
jupyter notebook notebooks/cleaner_eda.ipynb
```

Then run the cells in order to get predictions and tournament simulation results.

---

## Option 3: Create a Prediction Script

Create a file called `predict.py`:

```python
from src.worldcup_predictor import WorldCupPredictor
import pandas as pd

# Initialize predictor
predictor = WorldCupPredictor()

# Load raw data
matches = pd.read_csv("data/raw/matches.csv")
teams = pd.read_csv("data/raw/teams.csv")
tournaments = pd.read_csv("data/raw/tournaments.csv")

# Prepare data
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

# Train model
predictor.train_model()
predictor.evaluate_model()
predictor.feature_importance()
predictor.save_model()

print("\n" + "="*60)
print("MAKING PREDICTIONS")
print("="*60)

# Predict single match
prediction = predictor.predict_match("Brazil", "Germany")
print(f"\nMatch Prediction: {prediction['team_a']} vs {prediction['team_b']}")
print(f"Result: {prediction['result']}")

# Predict with probabilities
proba = predictor.predict_match_proba("Brazil", "Germany", stage_weight=4)
print(f"\nProbabilities:")
print(f"  {proba['team_a']} Win: {proba['team_a_win']:.2%}")
print(f"  Draw: {proba['draw']:.2%}")
print(f"  {proba['team_b']} Win: {proba['team_b_win']:.2%}")

# Tournament simulation
print("\n" + "="*60)
print("TOURNAMENT SIMULATION")
print("="*60)

predictor.load_2026_teams()

for group in predictor.groups:
    predictor.simulate_group(group)
    print(f"Group {group} simulated")

qualifiers = predictor.get_group_qualifiers()
print(f"\n✅ {len(qualifiers['qualified'])} teams qualified")

# Monte Carlo simulation
print("\nRunning 10,000 simulations...")
mc_results = predictor.run_many_simulations(qualifiers, n_simulations=10000)

# Display results
print("\n" + "="*60)
print("CHAMPIONSHIP PROBABILITIES (Top 15)")
print("="*60)

for i, team_prob in enumerate(mc_results['probabilities'][:15], 1):
    print(f"{i:2d}. {team_prob['team']:20s} - {team_prob['probability']:6.2f}% ({team_prob['wins']:,} wins)")

# Plot results
predictor.plot_probabilities(mc_results, top_n=10)
```

**Run it:**
```bash
python predict.py
```

---

## Option 4: Interactive Python Shell

Open Python directly:

```bash
python
```

Then run:

```python
from src.worldcup_predictor import WorldCupPredictor
import pandas as pd

# Load data
predictor = WorldCupPredictor()
matches = pd.read_csv("data/raw/matches.csv")
teams = pd.read_csv("data/raw/teams.csv")
tournaments = pd.read_csv("data/raw/tournaments.csv")

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

# Get a prediction
result = predictor.predict_match("France", "Argentina")
print(result)

# Get probabilities
proba = predictor.predict_match_proba("France", "Argentina")
print(f"France win: {proba['team_a_win']:.2%}")
print(f"Draw: {proba['draw']:.2%}")
print(f"Argentina win: {proba['team_b_win']:.2%}")

# Exit
exit()
```

---

## Common Commands Summary

### 1. Prepare Data (if missing)
```bash
python main.py prepare-data
```

### 2. Train Model
```bash
python main.py train
```

### 3. Train Model with Custom Paths
```bash
python main.py train --raw-dir ./data/raw --model-dir ./models/worldcup_predictor
```

### 4. View Help
```bash
python main.py --help
python main.py train --help
```

---

## What to Expect

### After Training:

**Terminal Output:**
- Data loading confirmation
- Cleaning progress
- Feature engineering steps
- Model training progress (shows iteration scores)
- Evaluation metrics (Accuracy, Precision, Recall, F1)
- Confusion matrix
- Feature importance ranking
- Model save confirmation

### Files Created:
```
models/worldcup_predictor/
├── catboost_model.cbm          # The trained model
├── feature_columns.pkl         # Feature names
├── class_labels.pkl            # Output classes (-1, 0, 1)
├── current_elo.pkl             # Latest Elo ratings
├── team_history.pkl            # Team match history
├── h2h_history.pkl             # Head-to-head records
└── metadata.json               # Model metadata
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'dotenv'"
**Solution:**
```bash
uv pip install python-dotenv
```

### Error: "No such file or directory: 'data/raw/matches.csv'"
**Solution:**
```bash
python main.py prepare-data
```
This will download the data from the API.

### Error: "API request failed"
**Solution:**
- Check that `.env` file exists and contains valid `API_KEY`
- Verify internet connection
- Check API status at https://api.zafronix.com

### Model takes too long to train
**Solution:**
- This is normal (2-5 minutes)
- Or reduce iterations in `train_model()` call:
  ```python
  predictor.train_model(iterations=100)  # Instead of 500
  ```

---

## Next Steps

1. **Train the model:** `python main.py train`
2. **Run predictions:** Use Option 3 (create `predict.py`)
3. **View results:** Check terminal output or export to CSV
4. **Visualize:** Use `plot_probabilities()` method
5. **Integrate:** Use model in API or web app

---

## Quick Reference

| What | Command |
|------|---------|
| Train model | `python main.py train` |
| Check data | `python main.py prepare-data` |
| Open notebook | `jupyter notebook notebooks/cleaner_eda.ipynb` |
| Interactive shell | `python` then paste code |
| View model files | `ls -lh models/worldcup_predictor/` |
| View features | `cat models/worldcup_predictor/metadata.json` |

---

Happy predicting! 🏆⚽
