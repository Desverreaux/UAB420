import machine
import time

LED = machine.Pin("LED", machine.Pin.OUT)

def off():
    LED.off()

def on():
    LED.on()

def blink(on_ms, off_ms):
    LED.on()
    time.sleep_ms(on_ms)
    LED.off()
    time.sleep_ms(off_ms)

def boot():
    LED.off()
    blink(1000, 1000)
    blink(1000, 1000)
    blink(1000, 1000)
    blink(1000, 1000)
    time.sleep_ms(2000)

def wifi_connecting():
    LED.off()
    blink(500, 500)
    blink(500, 500)
    blink(500, 500)
    time.sleep_ms(1000)

def wifi_connect_failed():
    LED.off()
    for _ in range(6):
        blink(100, 100)
    time.sleep_ms(1000)

def post_data_started():
    LED.off()
    blink(100, 100)

def post_data_failed():
    LED.off()
    blink(100, 100)
    blink(100, 100)
    blink(100, 100)
    time.sleep_ms(1000)

def entering_ap_mode():
    LED.off()
    blink(250, 250)
    blink(250, 500)
    blink(250, 250)
    blink(250, 500)
    blink(1000, 100)
    time.sleep_ms(1000)
