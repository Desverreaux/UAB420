import machine
import time
import config as cfg_mod
import wifi
import soil_sensor as sensor
import api

print("\n" + "=" * 50)
print("Soil sensor firmware v1.0.0 — booting")
print("=" * 50)

cfg = cfg_mod.load()
print(cfg)

if cfg is None:
    print("[main] no config found — halting. Upload config.json and reboot.")
    raise SystemExit

# connect to wifi

connected = wifi.connect(cfg)

if not connected:
    print("[main] WiFi failed — wiping credentials and rebooting.")
    print("[main] check SSID and password in config.json")
    cfg_mod.wipe_wifi(cfg)
    time.sleep(2)
    machine.reset()

while connected:

    cfg["_rssi"] = wifi.rssi()

    wifi.sync_time()

    timestamp = wifi.timestamp_iso()

    reading = sensor.read(cfg)

    success = api.post_reading(cfg, reading, timestamp)

    if not success:
        print("POST failed")

    sleep_time = 10
    time.sleep(sleep_time)