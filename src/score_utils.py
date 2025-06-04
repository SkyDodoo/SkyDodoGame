# score_utils.py
# ---------------------------------
# Utility functions for loading and saving high scores

import os

HIGHSCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))