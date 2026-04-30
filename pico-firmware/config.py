'''
Functions to save, load, and modify the config.json file.
'''

import json

CONFIG_PATH = "config.json"

def load():
    '''
    Attempts to open the config.json file.
    Returns the values from the JSON as a dictionary on success.
    Returns None on failure. 
    '''
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
    '''
    Saves the config file if changes have been made.
    Return True on success and False on failure.
    '''
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(cfg, f)
        print("[config] saved")
        return True
    except OSError as e:
        print(f"[config] save failed: {e}")
        return False

def has_wifi(cfg):
    '''
    Checks if the config file has WiFi credentials.
    Returns True if so and False if not.
    '''
    try:
        return bool(cfg["wifi"]["ssid"] and cfg["wifi"]["password"])
    except (KeyError, TypeError):
        return False
    
def create_default_config():
    '''
    Creates a new config file if it happens to be missing.
    This config file contains default values. 
    Returns True on success and False on failure.
    '''
    data = {
        "wifi": {
            "ssid": "YOUR_WIFI_SSID",
            "password": "YOUR_WIFI_PASSWORD"
        },
        "api": {
            "base_url": "http://uab420.desverreaux.com",
            "endpoint_reading": "/api/SendMoistureData",
            "key": ""
        },
        "sensor": {
            "id": "6",
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
    '''
    Clears the WiFi information from the config file.
    '''
    cfg["wifi"]["ssid"] = ""
    cfg["wifi"]["password"] = ""
    save(cfg)
