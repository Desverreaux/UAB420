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

# URL-decode form values (e.g. "My+WiFi" -> "My WiFi", "%20" -> " ", etc.)
def url_decode(value):
    value = value.replace("+", " ")
    out = ""
    i = 0
    while i < len(value):
        ch = value[i]
        if ch == "%" and i + 2 < len(value):
            try:
                out += chr(int(value[i + 1:i + 3], 16))
                i += 3
                continue
            except ValueError:
                pass
        out += ch
        i += 1
    return out

# Parse the form data from the POST request body and return a dictionary of parameters
def parse_form(data):
    try:
        body = data.split("\r\n\r\n")[1]
        params = {}
        for pair in body.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                params[url_decode(k)] = url_decode(v)
        return params
    except:
        return {}
    

# Save the WiFi credentials to a config file. Returns True on success, False on failure.
# TODO: maybe replace with config.py module.
def save_config(ssid, password):
    try:
        with open("config.json", "r") as f:
            config = ujson.load(f)
    except:
        config = {}
    config["wifi"] = config.get("wifi", {})
    config["wifi"]["ssid"] = ssid
    config["wifi"]["password"] = password
    config["wifi"]["configured"] = True
    try:
        with open("config.json", "w") as f:
            ujson.dump(config, f)
        return True
    except OSError as e:
        print("config save failed:", e)
        return False
    

# HTTP routing function to handle incoming requests and return appropriate responses based on the URL and method
def handle_request(request):
    global REBOOT_AT_MS
    request = request.decode()
    request_line = request.split("\r\n", 1)[0]

    # Captive portal triggers for common Android/iOS/Windows probes.
    portal_paths = (
        "/generate_204",
        "/hotspot-detect.html",
        "/ncsi.txt",
        "/connecttest.txt",
        "/redirect",
        "/canonical.html",
        "/success.txt",
        "/fwlink",
    )
    if any(path in request_line for path in portal_paths):
        return http_response(
            "",
            status="302 Found",
            headers=[f"Location: http://{AP_IP}/"],
        )

    # Config form submission
    if "POST /configure" in request:
        params = parse_form(request)

        ssid = params.get("ssid", "").strip()
        password = params.get("password", "")

        if not ssid:
            return http_response(
                "<h3>SSID is required.</h3><p><a href='/'>Go back</a></p>",
                status="400 Bad Request",
            )

        print("Received config for SSID:", ssid)

        if save_config(ssid, password):
            REBOOT_AT_MS = time.ticks_add(time.ticks_ms(), REBOOT_DELAY_MS)
            return http_response(success_page(ssid))
        return http_response(
            "<h3>Failed to save config.</h3><p><a href='/'>Try again</a></p>",
            status="500 Internal Server Error",
        )

    # Default: show config page
    return http_response(config_page())


# Read the full HTTP request from the client socket, including headers and body (if Content-Length is specified).
def read_http_request(cl, max_bytes=4096):
    data = b""

    # Read until we have headers.
    while b"\r\n\r\n" not in data and len(data) < max_bytes:
        try:
            chunk = cl.recv(1024)
        except OSError as e:
            if getattr(e, "errno", None) == 11:  # EAGAIN
                continue
            raise
        if not chunk:
            break
        data += chunk

    header_end = data.find(b"\r\n\r\n")
    if header_end == -1:
        return data

    # MicroPython decode() has no errors= kwarg; HTTP headers are ASCII/UTF-8.
    headers = data[:header_end].decode().split("\r\n")
    content_length = 0
    for line in headers[1:]:
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":", 1)[1].strip())
            except ValueError:
                content_length = 0
            break

    body = data[header_end + 4:]
    remaining = content_length - len(body)
    while remaining > 0 and len(data) < max_bytes:
        try:
            chunk = cl.recv(min(1024, remaining))
        except OSError as e:
            if getattr(e, "errno", None) == 11:  # EAGAIN
                continue
            raise
        if not chunk:
            break
        body += chunk
        remaining -= len(chunk)

    return data[:header_end + 4] + body


# Handle a DNS query by returning a response that points all domains to the AP IP address, enabling captive portal functionality.
def handle_dns_query(data):
    if len(data) < 12:
        return None

    # Copy transaction ID from query.
    txid = data[0:2]

    # Build a basic standard response with recursion desired/available bits.
    flags = b"\x81\x80"
    qdcount = data[4:6]
    ancount = qdcount
    nscount = b"\x00\x00"
    arcount = b"\x00\x00"
    header = txid + flags + qdcount + ancount + nscount + arcount

    # Find the end of the question section.
    idx = 12
    while idx < len(data) and data[idx] != 0:
        idx += 1 + data[idx]
    if idx + 5 >= len(data):
        return None
    question_end = idx + 5
    question = data[12:question_end]

    # Name pointer to original question at offset 12 (0xC00C).
    answer_name = b"\xc0\x0c"
    answer_type = b"\x00\x01"    # A record
    answer_class = b"\x00\x01"   # IN
    ttl = b"\x00\x00\x00\x1e"    # 30 seconds
    rdlength = b"\x00\x04"
    rdata = bytes(int(part) for part in AP_IP.split("."))

    answer = answer_name + answer_type + answer_class + ttl + rdlength + rdata
    return header + question + answer