import json
import os

# Cross-platform user-specific settings path
SETTINGS_DIR = os.path.join(os.path.expanduser("~"), ".skydodo")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"volume": 0.5}  # default

def save_settings(settings):
    os.makedirs(SETTINGS_DIR, exist_ok=True)  # Ensure the dir exists
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)
