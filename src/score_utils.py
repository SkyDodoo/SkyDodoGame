# score_utils.py
# ---------------------------------
# Utility functions for loading and saving high scores

import os

HIGHSCORE_FILE = "highscore.txt"

# Method: load_high_score
# -------------------------------------------------------------
# Reads the high score from the high score file.
# Returns the stored score as an integer.
# If the file does not exist or contains invalid data, returns 0.
def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

# Method: save_high_score
# score - integer score to be saved
# -------------------------------------------------------------
# Writes the given score to the high score file.
# Overwrites any existing content with the new score.
def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))