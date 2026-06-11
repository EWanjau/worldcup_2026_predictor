# How to Run World Cup Predictor - Simple Instructions

## 🎯 Three Ways to Get Predictions

### **Option 1: Simplest (Recommended for First Time)**

Open terminal and run:

```bash
python example_predict.py
```

**What happens:**
- Loads data automatically
- Trains the model with detailed progress
- Makes match predictions for Brazil vs Germany, France vs Argentina, etc.
- Simulates entire 2026 World Cup tournament (1000 times)
- Shows championship probabilities
- Displays a chart of top 10 teams

**Duration:** 3-7 minutes

**Terminal output will show:**
```
[1/9] Loading data files...
[2/9] Initializing predictor...
[3/9] Cleaning data...
[4/9] Building features...
[5/9] Preparing training data...
[6/9] Training CatBoost model...
[7/9] Evaluating model...
[8/9] Feature importance analysis...
[9/9] Make predictions...

======================================================================
  MATCH PREDICTIONS
======================================================================

Brazil              vs Germany
  Prediction: Brazil Win
  Probabilities:
    • Brazil Win: 65.23%
    • Draw:       18.45%
    • Germany Win: 16.32%

...

======================================================================
  CHAMPIONSHIP PROBABILITIES
======================================================================

Top 20 teams by championship probability:

 1. France                        32.12%  ████████████████████...
 2. Argentina                     21.34%  ████████████...
 3. Brazil                        18.56%  ███████████...
...
```

---

### **Option 2: Using Main Command**

```bash
python main.py train
```

**What happens:**
- Trains the model
- Shows evaluation metrics (Accuracy, Precision, Recall, F1)
- Shows confusion matrix
- Shows feature importance ranking
- Saves model for later use

**Duration:** 2-5 minutes

---

### **Option 3: Using Notebook**

```bash
jupyter notebook notebooks/cleaner_eda.ipynb
```

**What happens:**
- Opens interactive notebook in browser
- Run cells one by one to see results
- Already has trained model example

---

## 🔧 Pre-flight Check

Before running, check everything is set up:

```bash
python quick_test.py
```

**Should show:**
```
[✓] Checking .env file...
  ✓ .env file exists with API_KEY

[✓] Checking data files...
  ✓ data/raw/matches.csv
  ✓ data/raw/teams.csv
  ✓ data/raw/tournaments.csv

[✓] Checking source files...
  ✓ src/worldcup_predictor.py
  ✓ api/client.py
  ✓ config.py
  ✓ main.py

[✓] Checking Python dependencies...
  ✓ pandas
  ✓ numpy
  ✓ catboost
  ✓ sklearn
  ✓ matplotlib
  ✓ requests
  ✓ dotenv

[✓] Checking config loading...
  ✓ API_KEY loaded: zwc_free_f...
  ✓ BASE_URL loaded: https://api.zafronix.com/fifa/worldcup/v1
  ✓ HEADERS loaded with 2 fields

======================================================================
  SETUP CHECK COMPLETE
======================================================================

✓ All checks passed! You're ready to run:
  • python main.py train
  • python example_predict.py
  • jupyter notebook notebooks/cleaner_eda.ipynb
```

If all green ✓, you're good to go!

---

## 📊 What Results Mean

### Model Accuracy
- **Accuracy: 0.52** means the model correctly predicts 52% of matches
- Better than random (33%), good for a 3-outcome problem

### Match Probabilities
When you see:
```
Brazil vs Germany
  • Brazil Win: 65.23%
  • Draw:       18.45%
  • Germany Win: 16.32%
```

It means:
- Model thinks Brazil has 65% chance to win
- 18% chance it ends in a draw
- 16% chance Germany wins
- All three add to 100%

### Championship Probability
When you see:
```
1. France           32.12%
2. Argentina        21.34%
3. Brazil           18.56%
```

It means:
- In 10,000 simulations of the tournament:
  - France won ~3,212 times (32.12%)
  - Argentina won ~2,134 times (21.34%)
  - Brazil won ~1,856 times (18.56%)
- Top 3 teams win 72% of championships combined

---

## 🚨 If Something Goes Wrong

### Error: "ModuleNotFoundError: No module named 'dotenv'"
```bash
uv pip install python-dotenv
python quick_test.py
python example_predict.py
```

### Error: "No such file or directory: 'data/raw/matches.csv'"
```bash
python main.py prepare-data
python example_predict.py
```

### Error: "API request failed" or "401 Unauthorized"
```bash
# Check .env has your API key
cat .env

# If empty or wrong, update it:
echo "API_KEY=zwc_free_fddf1b15898bf77b9f29f7f1" > .env
echo "BASE_URL=https://api.zafronix.com/fifa/worldcup/v1" >> .env

python example_predict.py
```

### Takes too long to train
```bash
# This is normal (2-5 minutes)
# You can check progress in the terminal output
# Or reduce iterations in example_predict.py:

# Find this line:
predictor.train_model(iterations=200)

# Change 200 to 50:
predictor.train_model(iterations=50)
```

---

## 📋 Quick Reference

| Command | What it does | Duration |
|---------|-------------|----------|
| `python quick_test.py` | Check setup | < 1 sec |
| `python main.py train` | Train model only | 2-5 min |
| `python example_predict.py` | Full training + predictions | 3-7 min |
| `python main.py prepare-data` | Download data from API | 2-5 min |

---

## 📁 Files Explained

**After running, you'll create:**

```
models/worldcup_predictor/
├── catboost_model.cbm      ← The trained model (main file)
├── metadata.json           ← Model information
├── feature_columns.pkl     ← Feature names
├── class_labels.pkl        ← Output classes (-1, 0, 1)
├── current_elo.pkl         ← Latest Elo ratings
├── team_history.pkl        ← Team statistics
└── h2h_history.pkl         ← Head-to-head records

catboost_info/
├── catboost_training.json  ← Training progress
├── learn_error.tsv         ← Training errors
├── test_error.tsv          ← Test errors
└── time_left.tsv           ← Training time estimate
```

---

## 💡 Tips

1. **First time?** Run `python example_predict.py` - it shows everything

2. **Want to understand the process?** Read the commented cells in `notebooks/cleaner_eda.ipynb`

3. **Want custom predictions?** Edit `example_predict.py` and change the team names:
   ```python
   matchups = [
       ("Your Team A", "Your Team B"),
       ("France", "Spain"),
   ]
   ```

4. **Training taking time?** That's normal! You can see progress in terminal

5. **Want to save results?** Add at end of script:
   ```python
   df = pd.DataFrame(results)
   df.to_csv("my_predictions.csv", index=False)
   ```

---

## ✅ Summary

**To run predictions:**

```bash
# 1. Check setup (optional but recommended)
python quick_test.py

# 2. Run predictions
python example_predict.py

# 3. Wait 3-7 minutes
# 4. See results in terminal
# 5. View probability chart
```

**That's it!** 🎉

---

## 📖 For More Details

- **TERMINAL_GUIDE.md** - Detailed terminal instructions
- **QUICK_START.md** - Multiple ways to run the project
- **README.md** - Full project documentation
- **API_KEY_FLOW.md** - How API credentials are loaded

---

**Happy predicting! ⚽🏆**
