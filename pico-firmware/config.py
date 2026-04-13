import json

CONFIG_PATH = "config.json"

def load():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except OSError:
        print("[config] config.json not found")
        return None
    except ValueError:
        print("[config] config.json is malformed")
        return None

def save(cfg):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(cfg, f)
        print("[config] saved")
        return True
    except OSError as e:
        print(f"[config] save failed: {e}")
        return False

def has_wifi(cfg):
    try:
        return bool(cfg["wifi"]["ssid"] and cfg["wifi"]["password"])
    except (KeyError, TypeError):
        return False

def wipe_wifi(cfg):
    cfg["wifi"]["ssid"] = ""
    cfg["wifi"]["password"] = ""
    save(cfg)
