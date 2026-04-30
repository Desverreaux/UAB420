Everything in the pico-firmware folder pertains to the functioning of the Raspberry Pi Pico itself.
These are the files to be loaded onto the Pico.

--- LOADING AND RUNNING INSTRUCTIONS ---

If using VSCode and the MicroPico extension, the project can be loaded onto the Pico by:
    ctrl+shift+p > MicroPico: Connect
    right click pico-firmware folder > Initialize MicroPico project
    right click pico-firmware folder again > Upload project to Pico
    While the main.py file is open, right click main.py in the file explorer > Run current file on Pico

If all files have previously been loaded onto the Pico, the Pico can be plugged into a power source and the main.py file will run automatically.

--- FILE OVERVIEW ---

api.py
    Everything necessary for communications between the Pico and the API.

captive_portal.py
    Creates a captive portal. The captive portal creates a WiFi access point that can be connected to by the user.
    The user inputs their WiFi credentials and said credentials are saved to the config.json file.

config.json
    Necessary configuration values for connecting the Pico to WiFi and connecting to the API.
    Also contains configuation for soil sensor calibration and frequency of data collection.

config.py
    File containing methods to manage and modify the config.json file.

main.py
    The main operating file. Starts the Pico, connects the Pico to WiFi (or runs the captive portal
    if it cannot connect to a WiFi network), and routinely sends moisture sensor data to the API.

soil_sensor.py
    Methods to take moisture readings, parse them into a percentage format, and return the values.

status_led.py
    Contains various LED flashing patterns to signal what actions the Pico is currently taking.

wifi.py
    Methods for connecting the Pico to WiFi and returning timestamp data.


