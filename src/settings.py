# src/settings.py

import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"volume": 0.5}  # default

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)
