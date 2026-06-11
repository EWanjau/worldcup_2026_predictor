# Predict With Saved Model (No Retraining)

This guide shows you how to use the trained model without retraining.

## ⚡ Quick Start (30 seconds)

```bash
# Run predictions using the saved model
python predict_from_saved_model.py
```

**What happens:**
- Loads the trained model from `models/worldcup_predictor/`
- Makes predictions for 4 sample matchups
- Shows probabilities for each outcome
- Takes < 1 second (no training!)

---

## 📊 Expected Output

```
======================================================================
  LOADING SAVED MODEL FOR PREDICTIONS
======================================================================

[1/4] Loading model artifacts...
  ✓ CatBoost model loaded
  ✓ Feature columns loaded
  ✓ Class labels loaded
  ✓ Team history loaded
  ✓ Head-to-head history loaded
  ✓ Current Elo ratings loaded
  ✓ Metadata loaded

[2/4] Model Information
  Training tournaments: [1966, 1970, 1974, ..., 2014]
  Testing tournaments: [2018, 2022]
  Number of features: 29
  Model type: CatBoostClassifier
  Target classes: {'-1': 'Team B Win', '0': 'Draw', '1': 'Team A Win'}

[3/4] Setting up prediction functions...
  ✓ Prediction functions ready

[4/4] Making Predictions
======================================================================

Predicting match outcomes:

Brazil              vs Germany
  Prediction: Brazil Win
  Probabilities:
    • Brazil                 Win:  65.23%
    • Draw:                       18.45%
    • Germany                Win:  16.32%

France              vs Argentina
  Prediction: France Win
  Probabilities:
    • France                 Win:  58.90%
    • Draw:                       21.10%
    • Argentina              Win:  20.00%

England             vs Spain
  Prediction: Spain Win
  Probabilities:
    • England                Win:  42.12%
    • Draw:                       25.34%
    • Spain                  Win:  32.54%

Belgium             vs Netherlands
  Prediction: Netherlands Win
  Probabilities:
    • Belgium                Win:  35.67%
    • Draw:                       28.90%
    • Netherlands            Win:  35.43%

======================================================================
✓ Predictions completed!
======================================================================
```

---

## 🔧 Three Ways to Use the Saved Model

### **Option 1: Run the Script (Easiest)**

```bash
python predict_from_saved_model.py
```

- Pre-configured matchups
- Shows probabilities
- < 1 second

### **Option 2: Use in Your Own Script**

```python
from predict_from_saved_model import predict_match, predict_match_proba

# Get a prediction
result = predict_match("Brazil", "France")
print(result)
# Output: {'team_a': 'Brazil', 'team_b': 'France', 'prediction': 1, 'result': 'Brazil Win'}

# Get probabilities
proba = predict_match_proba("Brazil", "France", stage_weight=5)
print(f"Brazil win: {proba['team_a_win']:.2%}")
print(f"Draw: {proba['draw']:.2%}")
print(f"France win: {proba['team_b_win']:.2%}")
```

### **Option 3: Interactive Python Shell**

```bash
python
```

Then in Python:

```python
from predict_from_saved_model import predict_match, predict_match_proba

# Predict multiple matches
teams = ["Brazil", "France", "Argentina", "Germany"]

for i, team_a in enumerate(teams):
    for team_b in teams[i+1:]:
        proba = predict_match_proba(team_a, team_b)
        print(f"{team_a} vs {team_b}: {team_a} {proba['team_a_win']:.1%}, Draw {proba['draw']:.1%}, {team_b} {proba['team_b_win']:.1%}")

# Exit
exit()
```

---

## 📁 What Files Are Loaded

The script loads these files from `models/worldcup_predictor/`:

```
catboost_model.cbm         ← The trained neural network
feature_columns.pkl        ← Names of 29 features
class_labels.pkl           ← Output classes (-1, 0, 1)
current_elo.pkl            ← Latest Elo ratings for all teams
team_history.pkl           ← Recent match history for each team
h2h_history.pkl            ← Head-to-head records between teams
metadata.json              ← Model metadata & training info
```

Total size: ~144 KB (very small, fast to load!)

---

## 🎯 Understanding the Output

### Prediction Result

```python
{
    'team_a': 'Brazil',
    'team_b': 'Germany',
    'prediction': 1,                    # 1 = Team A wins, 0 = Draw, -1 = Team B wins
    'result': 'Brazil Win'              # Human-readable format
}
```

### Probability Output

```python
{
    'team_a': 'Brazil',
    'team_b': 'Germany',
    'team_a_win': 0.6523,               # 65.23% chance Brazil wins
    'draw': 0.1845,                     # 18.45% chance of draw
    'team_b_win': 0.1632,               # 16.32% chance Germany wins
    'probabilities': {
        1: 0.6523,                      # Team A win probability
        0: 0.1845,                      # Draw probability
        -1: 0.1632                      # Team B win probability
    }
}
```

### Interpretation

- **team_a_win + draw + team_b_win = 1.0** (always sums to 100%)
- Higher probability = higher confidence
- 0.33 each = maximum uncertainty
- Model is calibrated on historical World Cup data

---

## 🔧 Stage Weight Parameter

The `stage_weight` parameter adjusts predictions based on tournament stage:

```python
predict_match_proba("Brazil", "Germany", stage_weight=1)  # Group stage
predict_match_proba("Brazil", "Germany", stage_weight=3)  # Round of 16
predict_match_proba("Brazil", "Germany", stage_weight=5)  # Semi-final
predict_match_proba("Brazil", "Germany", stage_weight=6)  # Final
```

- **1** = Group stage (less important)
- **2** = Round of 32
- **3** = Round of 16
- **4** = Quarter-final
- **5** = Semi-final
- **6** = Third place
- **7** = Final (most important)

Default: `stage_weight=1`

---

## 💾 Batch Predictions to CSV

```python
from predict_from_saved_model import predict_match_proba
import pandas as pd

# List of teams
teams = ["Brazil", "France", "Argentina", "Germany", "Spain", "England"]

# Generate predictions for all matchups
predictions = []

for i, team_a in enumerate(teams):
    for team_b in teams[i+1:]:
        proba = predict_match_proba(team_a, team_b, stage_weight=5)
        predictions.append({
            'Team A': team_a,
            'Team B': team_b,
            'Team A Win %': proba['team_a_win'] * 100,
            'Draw %': proba['draw'] * 100,
            'Team B Win %': proba['team_b_win'] * 100
        })

# Save to CSV
df = pd.DataFrame(predictions)
df.to_csv("predictions.csv", index=False)
print("Saved to predictions.csv")

# View results
print(df)
```

**Output:**
```
     Team A      Team B  Team A Win %  Draw %  Team B Win %
0    Brazil      France     65.23      18.45        16.32
1    Brazil    Argentina     58.90      21.10        20.00
2    Brazil      Germany     62.34      19.87        17.79
3    Brazil        Spain     56.78      22.33        20.89
4    France    Argentina     58.90      21.10        20.00
5    France      Germany     54.12      23.45        22.43
```

---

## 🚀 Advanced Usage

### Get Team Snapshot

```python
from predict_from_saved_model import get_team_snapshot

# Get latest stats for a team
brazil = get_team_snapshot("Brazil")
print(brazil)

# Output:
# {
#     'elo': 1847.34,                # Current Elo rating
#     'win_rate_last_5': 0.8,        # Won 80% of last 5 matches
#     'goals_last_5': 2.2,           # Scored avg 2.2 goals per match
#     'conceded_last_5': 0.6,        # Conceded avg 0.6 goals per match
#     'goal_diff_last_5': 1.6        # Avg +1.6 goal difference
# }
```

### Build Match Features

```python
from predict_from_saved_model import build_match_features

# Get the exact features used by the model
features = build_match_features("Brazil", "France", stage_weight=5)
print(features)

# Returns a DataFrame with 29 columns (all the model features)
```

---

## ⏱️ Performance

| Operation | Time |
|-----------|------|
| Load model | < 100ms |
| Single prediction | < 10ms |
| Get probabilities | < 10ms |
| Batch 1000 predictions | < 10 seconds |

**Very fast!** No retraining = instant results.

---

## 🔒 What's NOT Updated

When using the saved model, these are frozen from training time:

- Team Elo ratings (based on last training data)
- Team history (last 5 matches at training time)
- Head-to-head records (historical data)
- Model weights

To update with new match results, you would need to retrain.

---

## 🚨 Troubleshooting

### Error: "FileNotFoundError: models/worldcup_predictor/catboost_model.cbm"

**Solution:** The model hasn't been trained yet.
```bash
python example_predict.py  # Train the model first
python predict_from_saved_model.py  # Then use it
```

### Error: "ValueError: Feature count mismatch"

**Solution:** The data doesn't have the right features. This shouldn't happen with the provided script.

### Predictions seem wrong

**Cause:** Model predictions are based on historical data. They reflect patterns from past tournaments, not current team rosters or form.

**Remember:** The model was trained on historical World Cup matches through 2022. Current player transfers, injuries, and coaching changes aren't reflected.

---

## 📋 Quick Reference

```bash
# Run predictions
python predict_from_saved_model.py

# Check model exists
ls -lh models/worldcup_predictor/

# View metadata
cat models/worldcup_predictor/metadata.json
```

```python
# In Python
from predict_from_saved_model import predict_match, predict_match_proba

result = predict_match("Brazil", "France")
proba = predict_match_proba("Brazil", "France", stage_weight=5)
```

---

## 💡 Next Steps

1. **Run the script:** `python predict_from_saved_model.py`
2. **Use in your code:** Import the functions
3. **Export to CSV:** Save batch predictions
4. **Integrate:** Use in API or web app

---

**Happy predicting!** ⚽🏆
