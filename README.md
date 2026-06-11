# World Cup 2026 Predictor

A machine learning project that predicts FIFA World Cup 2026 match outcomes using historical tournament data and advanced predictive modeling techniques.

## Project Overview

This project builds a **CatBoost classification model** to predict World Cup match results (home win, draw, or away win) based on historical data from past tournaments. The model incorporates multiple feature categories including Elo ratings, team form, head-to-head records, and historical tournament performance to generate predictions for the 2026 World Cup.

The predictor then simulates the entire 2026 World Cup tournament structure (group stage → knockout rounds → final) using Monte Carlo simulations to estimate championship probabilities for each team.

## Dataset

The project uses three primary data sources (CSV format):

- **matches.csv** - Historical World Cup match records (1,068 matches)
  - Match dates, teams, scores, tournament stages
  - Data spans multiple World Cup tournaments

- **teams.csv** - Team historical performance (537 records)
  - Tournament appearances, final positions
  - Knockout stage progression data

- **tournaments.csv** - World Cup tournament metadata (23 records)
  - Tournament years and information

## Getting Started

### Prerequisites

- Python 3.12+
- Dependencies listed in `pyproject.toml`

### Installation

1. Clone the repository
2. Install dependencies using `uv`:
   ```bash
   uv pip install -e .
   ```

### Running the Project

#### 1. Prepare Data

Ensure raw CSV files exist in `data/raw/`, or download them from the API:

```bash
python main.py prepare-data
```

This will:
- Check for required CSV files
- Download data from the API if files are missing

#### 2. Train the Model

Run the full training pipeline:

```bash
python main.py train
```

This executes all stages:
- Data loading and cleaning
- Feature engineering (Elo ratings, rolling stats, head-to-head records, historical metrics)
- Feature selection
- Train/test split (time-based)
- Model training with CatBoost
- Model evaluation and feature importance analysis
- Model artifact export

**Optional arguments:**
```bash
python main.py train --raw-dir ./data/raw --model-dir ./models/worldcup_predictor
```

## Model Architecture

### Features (29 total)

The model uses a comprehensive feature set grouped by category:

**Elo Rating Features:**
- `home_team_elo` - Home team Elo rating before match
- `away_team_elo` - Away team Elo rating before match
- `elo_difference` - Elo rating advantage (home - away)

**Rolling Form Features (Last 5 Matches):**
- `home_win_rate_last_5`, `away_win_rate_last_5` - Win rate over recent matches
- `home_goals_last_5`, `away_goals_last_5` - Average goals scored
- `home_conceded_last_5`, `away_conceded_last_5` - Average goals conceded
- `home_goal_diff_last_5`, `away_goal_diff_last_5` - Goal difference trend

**Head-to-Head Features:**
- `head_to_head_games` - Total previous matchups between teams
- `head_to_head_win_rate` - Historical win rate in matchups
- `head_to_head_goal_difference` - Cumulative goal difference

**Historical Performance Features:**
- `home_historical_titles`, `away_historical_titles` - World Cup championships won
- `home_knockout_rate`, `away_knockout_rate` - Frequency of reaching knockout stages
- `home_average_finish`, `away_average_finish` - Average tournament finish position
- `home_world_cup_appearances`, `away_world_cup_appearances` - Total tournament appearances
- `home_semi_final_rate`, `away_semi_final_rate` - Frequency of reaching semi-finals
- `home_final_rate`, `away_final_rate` - Frequency of reaching finals

**Stage Weight:**
- `stage_weight` - Tournament stage importance (Group=1, R32=2, R16=3, QF=4, SF=5, Final=6)

### Model Configuration

- **Algorithm:** CatBoost Classifier (gradient boosting)
- **Iterations:** 500
- **Learning Rate:** 0.05
- **Tree Depth:** 6
- **Loss Function:** MultiClass (3 classes)
- **Train/Test Split:** Time-based (all tournaments except last 2 for training; last 2 tournaments for testing)

## Model Performance

### Evaluation Metrics

The model is evaluated on test data from the last 2 World Cup tournaments:

- **Accuracy** - Overall prediction correctness
- **Balanced Accuracy** - Accuracy weighted by class distribution
- **Precision (Macro)** - Per-class precision averaged
- **Recall (Macro)** - Per-class recall averaged
- **F1 Score (Macro)** - Harmonic mean of precision and recall

### Confusion Matrix

Shows prediction accuracy across the three outcome classes:
- Class 1: Home Team Win
- Class 0: Draw
- Class -1: Away Team Win

### What the Scores Mean

- **Accuracy (e.g., 0.52)** - The model correctly predicts the match outcome 52% of the time. Better than random (33%), this indicates the model captures real patterns in World Cup matches.

- **Balanced Accuracy** - Accounts for class imbalance. If different outcomes occur with different frequencies, balanced accuracy shows how well the model performs on each outcome type equally.

- **Precision** - Of all predictions made for a class (e.g., "Home Win"), what percentage were actually correct? High precision = fewer false positives.

- **Recall** - Of all actual instances of a class, what percentage did the model identify? High recall = fewer false negatives.

- **F1 Score** - Single metric balancing precision and recall. Useful for imbalanced datasets where you care about both false positives and false negatives.

## Feature Importance

The top features driving predictions are identified through CatBoost's feature importance calculation. These show which information most influences match outcome predictions. Features like Elo ratings, recent form, and historical performance typically rank highest.

## Tournament Simulation

### 2026 World Cup Structure

The simulator replicates the official tournament format:

**Group Stage (Phase 1):**
- 12 groups (A-L) with 4 teams each
- Round-robin format (each team plays 3 matches)
- Top 2 teams from each group advance
- Best 8 third-place teams also advance

**Knockout Rounds (Phase 2):**
- Round of 32 (16 matches)
- Round of 16 (8 matches)
- Quarterfinals (4 matches)
- Semifinals (2 matches)
- Final (1 match)

### Prediction Process

For each match:
1. Model predicts win probabilities for each outcome
2. Outcome randomly selected weighted by probabilities
3. Score generated based on outcome (e.g., home wins = [1-0, 2-0, 2-1, 3-1, 3-0])
4. Group tables updated with points and goal difference
5. Qualifiers determined by official FIFA rules

### Monte Carlo Simulations

The project runs multiple tournament simulations (typically 10,000) to estimate:
- **Team Win Probabilities** - Percentage chance each team wins the championship
- **Confidence Intervals** - Stability of predictions across simulations
- **Upset Probability** - Likelihood of unexpected tournament outcomes

### Interpretation of Results

The visualization plots the top 10 teams by championship probability:

**Example Output:**
```
Team                 Wins    Probability
France              3200     32.00%
Argentina           2100     21.00%
Brazil              1800     18.00%
Germany             950      9.50%
Belgium             600      6.00%
...
```

**What This Means:**
- France has a 32% chance of winning the 2026 World Cup based on historical patterns and current team strength
- Argentina at 21% reflects strong recent form and tournament experience
- Brazil at 18% shows competitive strength but slightly lower probability than France
- Probabilities sum to 100% across all 32 teams
- Higher variance between top teams = greater certainty about favorites
- Lower probabilities for weaker teams reflect historical underperformance

**Important Caveats:**
- Model is based on historical patterns; recent roster changes not captured
- Injuries, transfers, and coaching changes not considered
- Elo ratings based on matches through training date
- Home/away advantage not applicable in World Cup (neutral venues)

## Model Artifacts

After training, the following files are saved in `models/worldcup_predictor/`:

```
models/worldcup_predictor/
├── catboost_model.cbm          # Trained CatBoost model
├── feature_columns.pkl         # Feature names and order
├── class_labels.pkl            # Output class mapping (-1, 0, 1)
├── current_elo.pkl             # Latest Elo ratings for all teams
├── team_history.pkl            # Historical match records per team
├── h2h_history.pkl             # Head-to-head records by team pairs
└── metadata.json               # Model configuration and metadata
```

## File Structure

```
worldcup_2026_predictor/
├── data/
│   └── raw/                    # Raw CSV data files
├── models/
│   └── worldcup_predictor/     # Trained model artifacts
├── notebooks/
│   └── cleaner_eda.ipynb       # Exploratory data analysis
├── src/
│   └── worldcup_predictor.py   # Main predictor class
├── ingestion/
│   └── main_dataset_builder.py # API data download
├── main.py                     # Entry point
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## API Integration

The `WorldCupPredictor` class provides methods for:

**Single Match Prediction:**
```python
predictor.predict_match("Brazil", "Germany")
# Output: {"team_a": "Brazil", "team_b": "Germany", "prediction": 1, "result": "Brazil Win"}
```

**Match Probabilities:**
```python
predictor.predict_match_proba("Brazil", "Germany", stage_weight=4)
# Output: {"team_a": "Brazil", "team_b": "Germany", 
#          "team_a_win": 0.65, "draw": 0.20, "team_b_win": 0.15, ...}
```

**Tournament Simulation:**
```python
qualifiers = predictor.get_group_qualifiers()
results = predictor.simulate_tournament(qualifiers)
```

**Monte Carlo Simulations:**
```python
probabilities = predictor.run_many_simulations(qualifiers, n_simulations=10000)
predictor.plot_probabilities(probabilities, top_n=10)
```

## Dependencies

- **catboost** - Gradient boosting classifier
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning utilities
- **matplotlib** - Visualization
- **requests** - API calls
- **streamlit** - Web interface (optional)

## Development

### Running Notebooks

The EDA notebook (`notebooks/cleaner_eda.ipynb`) documents:
- Data loading and exploration
- Feature engineering walkthrough
- Model training and evaluation
- Tournament simulation examples

### Extending the Model

To improve predictions:
1. Add more feature categories (e.g., player ratings, recent friendlies)
2. Tune hyperparameters (learning rate, tree depth, iterations)
3. Adjust Elo K-factor for match importance
4. Implement player-level features
5. Add weather/altitude factors
6. Incorporate betting odds as features

## License

[Specify your license here]

## Contact

For questions or issues, contact: [Your contact information]

---

**Last Updated:** June 2026
**Model Version:** 1.0
**Data Through:** 2022 World Cup
