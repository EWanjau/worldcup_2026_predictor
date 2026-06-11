 # How to Use Saved Model (No Retraining)

Your trained model is saved and ready to use! Here's how to make predictions without retraining.

## ⚡ Quick Start (1 Line)

```bash
python predict_from_saved_model.py
```

**What happens:**
- Loads the saved model from `models/worldcup_predictor/` (~144 KB)
- Makes 4 sample match predictions
- Shows win probabilities for each team
- Takes < 1 second (no training!)

## 📊 Example Output

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
  Training tournaments: [1930, 1934, ..., 2014]
  Testing tournaments: [2018, 2022]
  Number of features: 27
  Model type: CatBoostClassifier

[3/4] Setting up prediction functions...
  ✓ Prediction functions ready

[4/4] Making Predictions
======================================================================

Predicting match outcomes:

Brazil               vs Germany
  Prediction: Brazil Win
  Probabilities:
    • Brazil Win:       38.37%
    • Draw:             30.19%
    • Germany Win:      31.43%

France               vs Argentina
  Prediction: France Win
  Probabilities:
    • France Win:       38.37%
    • Draw:             30.19%
    • Argentina Win:    31.43%

======================================================================
✓ Predictions completed!
======================================================================
```

## 🎯 Three Ways to Use

### 1️⃣ **Run the Script** (Easiest)

```bash
python predict_from_saved_model.py
```

- No coding needed
- Pre-configured matchups
- Shows results on terminal
- Duration: < 1 second

---

### 2️⃣ **Import Functions** (Recommended for Custom Use)

```python
from predict_from_saved_model import predict_match, predict_match_proba

# Single prediction
result = predict_match("Brazil", "France")
print(result)
# {'team_a': 'Brazil', 'team_b': 'France', 'prediction': 1, 'result': 'Brazil Win'}

# Probabilities
proba = predict_match_proba("Brazil", "France", stage_weight=5)
print(f"Brazil win: {proba['team_a_win']:.2%}")
print(f"Draw: {proba['draw']:.2%}")
print(f"France win: {proba['team_b_win']:.2%}")
```

---

### 3️⃣ **Interactive Python**

```bash
python
```

Then:

```python
from predict_from_saved_model import predict_match_proba

# Predict multiple matches
teams = ["Brazil", "France", "Argentina"]

for i, t1 in enumerate(teams):
    for t2 in teams[i+1:]:
        p = predict_match_proba(t1, t2)
        print(f"{t1:15s} vs {t2:15s}: {t1:10s} {p['team_a_win']:.1%}")

exit()
```

---

## 💻 Code Examples

### Example 1: Single Match Prediction

```python
from predict_from_saved_model import predict_match, predict_match_proba

# Get prediction
pred = predict_match("Brazil", "Germany", stage_weight=5)
print(f"Prediction: {pred['result']}")

# Get probabilities
proba = predict_match_proba("Brazil", "Germany", stage_weight=5)
print(f"Brazil win probability: {proba['team_a_win']:.2%}")
```

### Example 2: Batch Predictions to CSV

```python
from predict_from_saved_model import predict_match_proba
import pandas as pd

# All matchups for top teams
teams = ["Brazil", "France", "Argentina", "Germany", "Spain", "England"]

predictions = []
for i, t1 in enumerate(teams):
    for t2 in teams[i+1:]:
        p = predict_match_proba(t1, t2, stage_weight=5)
        predictions.append({
            'Team A': t1,
            'Team B': t2,
            'Team A Win %': p['team_a_win'] * 100,
            'Draw %': p['draw'] * 100,
            'Team B Win %': p['team_b_win'] * 100
        })

# Save to CSV
df = pd.DataFrame(predictions)
df.to_csv("my_predictions.csv", index=False)
print("✓ Saved to my_predictions.csv")
```

### Example 3: Find Strongest Teams

```python
from predict_from_saved_model import get_team_snapshot

teams = ["Brazil", "France", "Argentina", "Germany", "Spain", "England"]

# Get Elo ratings
ratings = []
for team in teams:
    snapshot = get_team_snapshot(team)
    ratings.append({'team': team, 'elo': snapshot['elo']})

# Sort by Elo
import pandas as pd
df = pd.DataFrame(ratings).sort_values('elo', ascending=False)
print(df)

# Output:
#        team      elo
# 0    Brazil  1847.34
# 1     Spain  1823.45
# 2    France  1812.34
```

---

## 📁 What's Loaded

The script loads these pre-trained files:

| File | Size | Purpose |
|------|------|---------|
| `catboost_model.cbm` | 25 KB | The trained neural network |
| `feature_columns.pkl` | 612 B | Names of 27 features |
| `class_labels.pkl` | 172 B | Output classes (-1, 0, 1) |
| `current_elo.pkl` | 1.7 KB | Latest Elo ratings |
| `team_history.pkl` | 61 KB | Recent match history |
| `h2h_history.pkl` | 36 KB | Head-to-head records |
| `metadata.json` | 1.4 KB | Model metadata |
| **TOTAL** | **~144 KB** | **Very fast!** |

---

## 🔧 Stage Weight Parameter

Adjust the tournament stage importance:

```python
predict_match_proba("Brazil", "France", stage_weight=1)   # Group stage
predict_match_proba("Brazil", "France", stage_weight=3)   # Round of 16
predict_match_proba("Brazil", "France", stage_weight=5)   # Semi-final
predict_match_proba("Brazil", "France", stage_weight=6)   # Final
```

- **stage_weight=1** = Group stage (least important)
- **stage_weight=3** = Round of 16
- **stage_weight=5** = Semi-final
- **stage_weight=6** = Final (most important)

---

## 📊 Understanding Results

### Prediction Format

```python
{
    'team_a': 'Brazil',
    'team_b': 'Germany',
    'prediction': 1,        # 1=Team A wins, 0=Draw, -1=Team B wins
    'result': 'Brazil Win'
}
```

### Probability Format

```python
{
    'team_a': 'Brazil',
    'team_b': 'Germany',
    'team_a_win': 0.3837,   # 38.37% chance
    'draw': 0.3019,         # 30.19% chance
    'team_b_win': 0.3143,   # 31.43% chance
    'probabilities': {
        1: 0.3837,          # Team A win
        0: 0.3019,          # Draw
        -1: 0.3143          # Team B win
    }
}
```

### Interpretation

- **All probabilities sum to 1.0** (100%)
- Higher probability = higher confidence
- ~0.33 for each = maximum uncertainty
- Based on historical World Cup patterns

---

## ⚡ Performance

| Operation | Time |
|-----------|------|
| Load model | ~100 ms |
| Single prediction | ~10 ms |
| Get probabilities | ~10 ms |
| 100 predictions | ~1 second |
| 1000 predictions | ~10 seconds |

**Much faster than training (which takes 3-7 minutes)!**

---

## 🚨 Troubleshooting

### Error: "FileNotFoundError: catboost_model.cbm"

**Cause:** Model hasn't been trained yet

**Solution:**
```bash
python example_predict.py  # Train first
python predict_from_saved_model.py  # Then predict
```

### Error: "ValueError: Feature count mismatch"

**Cause:** Data doesn't have the right features

**Solution:** Use the provided `predict_from_saved_model.py` which handles this automatically

### Predictions seem off

**Remember:**
- Model is trained on historical data (1930-2022)
- Current team rosters/injuries not included
- Recent transfers not reflected
- Reflects historical patterns, not current form

---

## 💡 Tips

1. **Import the functions for reuse:**
   ```python
   from predict_from_saved_model import predict_match, predict_match_proba
   ```

2. **Batch process many predictions:**
   ```python
   for team_a, team_b in matchups:
       p = predict_match_proba(team_a, team_b)
       # Save or process result
   ```

3. **Export to CSV for analysis:**
   ```python
   df.to_csv("predictions.csv", index=False)
   ```

4. **Adjust stage_weight by tournament stage:**
   ```python
   for stage, weight in [("Group", 1), ("R16", 3), ("Final", 6)]:
       p = predict_match_proba(t1, t2, stage_weight=weight)
   ```

---

## 📋 Quick Command Reference

```bash
# Run predictions from terminal
python predict_from_saved_model.py

# Check model files exist
ls -lh models/worldcup_predictor/

# View model metadata
cat models/worldcup_predictor/metadata.json

# Python interactive
python

# In Python:
from predict_from_saved_model import predict_match_proba
p = predict_match_proba("Brazil", "France", stage_weight=5)
print(f"Brazil: {p['team_a_win']:.1%}")
```

---

## 🎯 Next Steps

1. **Run predictions:** `python predict_from_saved_model.py`
2. **Import functions:** Use in your own scripts
3. **Export results:** Save to CSV
4. **Integrate:** Use in API or web app

---

**The model is ready to use! No retraining needed.** ⚽🏆
