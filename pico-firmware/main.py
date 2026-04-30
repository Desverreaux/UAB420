'''
Main file. Runs on Pico startup.
Connects Pico to WiFi or starts a captive portal.
Reads moisture data and sends to API.

'''

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
    '''
    Pico enters AP mode, opening the captive portal and waiting for a connection.
    Once the portal has received data from the user, the Pico restarts.
    '''
    print("[main] starting AP mode")
    status_led.entering_ap_mode()
    portal.start_portal()

    time.sleep(2)
    machine.reset()

def connect_to_wifi(cfg, attempts=CONNECT_WIFI_ATTEMPTS):
    '''
    Pico attempts to connect to WiFi using the SSID and password in the config.json file.
    Will attempt a given number of times before stopping trying to connect. 
    '''
    print("[main] connecting to WiFi")
    for attempt in range(attempts):
        status_led.wifi_connecting()
        if wifi.connect(cfg):
            return True
        print(f"[main] WiFi connection attempt {attempt + 1} failed")
    return False
    

def boot():
    '''
    Starts both the status_led module and loads in the config file. It will attempt to connect to the WiFi in the config.
    If the config file does not exist, a default one will be created.
    If the config file has no WiFi information or cannot connect to the given WiFi, the Pico will enter AP mode.
    '''
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
        start_ap_mode()

    wifi.sync_time()
    return cfg

def run(cfg):
    '''
    The standard operating loop of the Pico, for after a WiFi connection has been established.
    If the Pico ever disconnects from the WiFi and cannot reconnect, it will enter AP mode.
    Otherwise, the Pico will take moisture readings at a regular interval specified by the config file and sends to the API.
    '''
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