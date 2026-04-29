import network
import ntptime
import time

CONNECT_TIMEOUT_S = 20


def connect(cfg):
    """
    Connect to WiFi using credentials from config.
    Returns True on success, False on failure.
    """
    ssid     = cfg["wifi"]["ssid"]
    password = cfg["wifi"]["password"]

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print(f"[wifi] already connected: {wlan.ifconfig()[0]}")
        return True

    print(f"[wifi] connecting to '{ssid}'...")
    wlan.connect(ssid, password)

    deadline = time.time() + CONNECT_TIMEOUT_S
    while not wlan.isconnected():
        if time.time() > deadline:
            print("[wifi] connection timed out")
            wlan.active(False)
            return False
        time.sleep_ms(500)

    ip = wlan.ifconfig()[0]
    rssi = wlan.status("rssi")
    print(f"[wifi] connected — IP={ip}  RSSI={rssi}dBm")
    return True


def is_wifi_connected():
    wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()


def rssi():
    wlan = network.WLAN(network.STA_IF)
    try:
        return wlan.status("rssi")
    except Exception:
        return None


def sync_time():
    """
    Sync RTC via NTP. Retry up to 3 times.
    Returns True on success.
    """
    for attempt in range(1, 4):
        try:
            ntptime.settime()
            t = time.localtime()
            print(f"[wifi] NTP sync OK — {t[0]}-{t[1]:02d}-{t[2]:02d} "
                  f"{t[3]:02d}:{t[4]:02d}:{t[5]:02d} UTC")
            return True
        except Exception as e:
            print(f"[wifi] NTP attempt {attempt} failed: {e}")
            time.sleep(1)
    print("[wifi] NTP sync failed — timestamps will be inaccurate")
    return False


def timestamp_iso():
    """
    Return current UTC time as ISO-8601 string.
    Falls back gracefully if clock not synced.
    """
    t = time.localtime()
    return (f"{t[0]}-{t[1]:02d}-{t[2]:02d}T"
            f"{t[3]:02d}:{t[4]:02d}:{t[5]:02d}Z")


def disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
