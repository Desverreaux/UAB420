import machine
import time
import config as cfg_mod
import wifi
import soil_sensor as sensor
import api
import captive_portal as portal
import status_led 


CONNECT_WIFI_ATTEMPTS = 3


def start_ap_mode():
    print("[main] starting AP mode")
    status_led.entering_ap_mode()
    portal.start_portal()

    time.sleep(2)
    machine.reset()

def connect_to_wifi(cfg, attempts=CONNECT_WIFI_ATTEMPTS):

    print("[main] connecting to WiFi")
    for attempt in range(attempts):
        status_led.wifi_connecting()
        if wifi.connect(cfg):
            return True
        print(f"[main] WiFi connection attempt {attempt + 1} failed")
        time.sleep(1)
    return False
    

def boot():
    print("\n" + "=" * 50)
    print("Soil sensor firmware v1.0.0 — booting")
    print("=" * 50)

    status_led.boot()

    cfg = cfg_mod.load()
    # print(cfg)

    if cfg is None:
        print("[main] no config found. Creating default config file.")
        if not cfg_mod.create_default_config():
            print("[main] failed to create default config file. Upload config.json and reboot.")
            raise SystemExit

    if not cfg_mod.has_wifi(cfg):
        print("[main] no WiFi config found — starting AP mode.")
        start_ap_mode()

    if not connect_to_wifi(cfg):
        print("[main] WiFi failed — starting AP mode.")
        status_led.wifi_connect_failed()
        time.sleep(2)
        start_ap_mode()

    wifi.sync_time()
    return cfg

def run(cfg):

    while True:
        if not wifi.is_wifi_connected():
            print("[main] WiFi disconnected - reconnecting...")
            if not connect_to_wifi(cfg):
                print("[main] WiFi failed — starting AP mode.")
                start_ap_mode()

        timestamp = wifi.timestamp_iso()
        reading = sensor.read(cfg)
        status_led.post_data_started()
        success = api.post_reading(cfg, reading, timestamp)
        if not success:
            print("[main] POST failed")
            status_led.post_data_failed()

        status_led.normal_mode()
        time.sleep(cfg["sensor"]["interval_minutes"] * 60)



cfg = boot()
run(cfg)