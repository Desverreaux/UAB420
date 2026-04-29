import urequests
import json
import config as cfg_mod


def post_reading(cfg, reading, timestamp):
    """
    POST sensor reading to the API.
    Expects server to return JSON with optional config block.
    Returns True on success, False on failure.
    """
    url = cfg["api"]["base_url"] + cfg["api"]["endpoint_reading"]

    payload = {
        "plantId":      cfg["sensor"]["id"],
        "moistureLevel":   reading["moisture_pct"],
        "raw_adc":        reading["raw_adc"],
        "timestamp":  timestamp,
        "firmware_version": cfg["firmware_version"],
        "rssi":           cfg.get("_rssi", None)
    }

    headers = {
        "Content-Type": "application/json"
    }

    api_key = cfg["api"].get("key", "")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    print(f"[api] POST {url}")
    print(f"[api] payload: {json.dumps(payload)}")

    try:
        res = urequests.post(url, data=json.dumps(payload), headers=headers)
        print(f"[api] response status: {res.status_code}")

        if res.status_code == 201:
            _handle_response(cfg, res)
            res.close()
            return True
        else:
            print(f"[api] unexpected status: {res.status_code}")
            res.close()
            return False

    except Exception as e:
        print(f"[api] request failed: {e}")
        return False


def _handle_response(cfg, res):
    """
    Parse server response and apply any config changes.
    Expected response shape:
    {
        "status": "ok",
        "config": {
            "interval_minutes": 30,
            "calibration": {
                "dry_raw": 45000,
                "wet_raw": 19000
            }
        }
    }
    """
    try:
        body = res.json()
    except Exception:
        print("[api] could not parse response body")
        return

    if body.get("status") != "ok":
        print(f"[api] server returned status: {body.get('status')}")

    server_cfg = body.get("config")
    if not server_cfg:
        return

    changed = False

    new_interval = server_cfg.get("interval_minutes")
    if new_interval and new_interval != cfg["sensor"]["interval_minutes"]:
        print(f"[api] interval updated: {cfg['sensor']['interval_minutes']} "
              f"→ {new_interval} min")
        cfg["sensor"]["interval_minutes"] = new_interval
        changed = True

    new_cal = server_cfg.get("calibration")
    if new_cal:
        if new_cal.get("dry_raw") and new_cal["dry_raw"] != cfg["sensor"]["calibration"]["dry_raw"]:
            print(f"[api] dry_raw updated: {cfg['sensor']['calibration']['dry_raw']} "
                  f"→ {new_cal['dry_raw']}")
            cfg["sensor"]["calibration"]["dry_raw"] = new_cal["dry_raw"]
            changed = True
        if new_cal.get("wet_raw") and new_cal["wet_raw"] != cfg["sensor"]["calibration"]["wet_raw"]:
            print(f"[api] wet_raw updated: {cfg['sensor']['calibration']['wet_raw']} "
                  f"→ {new_cal['wet_raw']}")
            cfg["sensor"]["calibration"]["wet_raw"] = new_cal["wet_raw"]
            changed = True

    if changed:
        cfg_mod.save(cfg)
        print("[api] config.json updated from server response")
    else:
        print("[api] no config changes from server")
