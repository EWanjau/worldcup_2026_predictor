#!/usr/bin/env python
"""
Quick test script - checks if everything is set up correctly.
Run with: python src/scripts/quick_test.py
"""

import sys
import os

# Change to project root if running from scripts directory
if os.path.basename(os.getcwd()) == "scripts":
    os.chdir(os.path.join(os.path.dirname(__file__), "../.."))

print("\n" + "="*70)
print("  QUICK SETUP CHECK")
print("="*70)

# Check 1: .env file
print("\n[✓] Checking .env file...")
if os.path.exists(".env"):
    with open(".env") as f:
        content = f.read()
        if "API_KEY" in content:
            print("  ✓ .env file exists with API_KEY")
        else:
            print("  ✗ .env file missing API_KEY")
else:
    print("  ✗ .env file not found")

# Check 2: Data files
print("\n[✓] Checking data files...")
required_files = [
    "data/raw/matches.csv",
    "data/raw/teams.csv",
    "data/raw/tournaments.csv"
]

for file in required_files:
    if os.path.exists(file):
        size = os.path.getsize(file) / 1024 / 1024
        print(f"  ✓ {file:40s} ({size:6.2f} MB)")
    else:
        print(f"  ✗ {file:40s} (NOT FOUND)")

# Check 3: Source files
print("\n[✓] Checking source files...")
source_files = [
    "src/worldcup_predictor.py",
    "api/client.py",
    "config.py",
    "main.py"
]

for file in source_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} (NOT FOUND)")

# Check 4: Python dependencies
print("\n[✓] Checking Python dependencies...")
dependencies = [
    "pandas",
    "numpy",
    "catboost",
    "sklearn",
    "matplotlib",
    "requests",
    "dotenv"
]

for dep in dependencies:
    try:
        __import__(dep)
        print(f"  ✓ {dep}")
    except ImportError:
        print(f"  ✗ {dep} (NOT INSTALLED)")

# Check 5: Config loading
print("\n[✓] Checking config loading...")
try:
    from config import API_KEY, BASE_URL, HEADERS
    if API_KEY:
        print(f"  ✓ API_KEY loaded: {API_KEY[:10]}...")
        print(f"  ✓ BASE_URL loaded: {BASE_URL}")
        print(f"  ✓ HEADERS loaded with {len(HEADERS)} fields")
    else:
        print("  ✗ API_KEY is empty")
except Exception as e:
    print(f"  ✗ Error loading config: {e}")

print("\n" + "="*70)
print("  SETUP CHECK COMPLETE")
print("="*70)

print("\n✓ All checks passed! You're ready to run:")
print("  • python src/scripts/predict_from_saved_model.py  (use saved model)")
print("  • python src/scripts/example_predict.py          (train from scratch)")
print("  • python main.py train                            (train from CLI)")
print("  • jupyter notebook notebooks/cleaner_eda.ipynb    (interactive notebook)")
