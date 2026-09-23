import json
import os

from wadllib.application import wadl_xpath

SETTINGS_PATH = os.path.join(os.path.expanduser('~'), '.settings.json')

DEFAULT_SETTINGS = {
    "window_width": 500,
    "window_height": 500,
    "theme": "dark",
    "last_file_opened": None,
}

def load_settings():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return DEFAULT_SETTINGS.copy()
    except json.JSONDecodeError:
        print("Setting file corrupted. Restore the default settings.")
        return DEFAULT_SETTINGS.copy()
    except OSError as e:
        print(f"Another error: {e}")
        return DEFAULT_SETTINGS.copy()

    merged = DEFAULT_SETTINGS.copy()
    merged.update(data)
    return merged

def save_settings(settings: dict):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except OSError as e:
        print(f"Settings not found: {e}")
