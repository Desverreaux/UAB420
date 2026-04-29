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
    
def create_default_config():
    data = {
        "wifi": {
            "ssid": "YOUR_WIFI_SSID",
            "password": "YOUR_WIFI_PASSWORD"
        },
        "api": {
            "base_url": "http://192.168.1.96:5000",
            "endpoint_reading": "/api/sensor/reading",
            "key": ""
        },
        "sensor": {
            "id": "sensor-01",
            "interval_minutes": 1,
            "calibration": {
                "dry_raw": 45000,
                "wet_raw": 19000
            }
        },
        "firmware_version": "1.0.0"
    }
    try:
        with open("config.json", "w") as f:
            json.dump(data, f)
            f.close()
    except OSError as e:
        print(f"[config] failed to create default config: {e}")
        return False
    else:
        print("[config] default config created")
        return True

def wipe_wifi(cfg):
    cfg["wifi"]["ssid"] = ""
    cfg["wifi"]["password"] = ""
    save(cfg)
