import network
import socket
import time
import ujson
import machine
import uselect

AP_SSID = "ThirstyPlant-Setup"
AP_PASSWORD = "ThirstyPlant123"
AP_IP = "192.168.4.1"
REBOOT_DELAY_MS = 6000
REBOOT_AT_MS = None


# Start the access point and configure the network settings
def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=AP_SSID, password=AP_PASSWORD)
    
    try:
        ap.ifconfig((AP_IP, "255.255.255.0", AP_IP, AP_IP))
    except Exception as e:
        print("AP ifconfig set failed:", e)

    while not ap.active():
        pass

    print("AP started:", AP_SSID)
    print("IP:", ap.ifconfig()[0])


def http_response(body, status="200 OK", content_type="text/html", headers=None):
    lines = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        "Cache-Control: no-store",
    ]
    if headers:
        lines.extend(headers)
    lines.append("")
    lines.append(body)
    return "\r\n".join(lines)

# Basic captive portal page with a form to submit WiFi credentials
# TODO: Add some styling later
def config_page():
    return """
    <html>
    <body>
        <h2>Configure WiFi</h2>
        <form action="/configure" method="post">
            SSID:<br>
            <input name="ssid"><br>
            Password:<br>
            <input name="password" type="password"><br><br>
            <input type="submit" value="Save">
        </form>
    </body>
    </html>
    """

# TODO: MAYBE add some styling here too...
def success_page(ssid):
    return f"""
    <html>
    <body>
        <h2>WiFi Saved</h2>
        <p>SSID: <b>{ssid}</b></p>
        <p>Your Pico is rebooting now. Reconnect to your normal WiFi and return to your sensor app in a few seconds.</p>
    </body>
    </html>
    """