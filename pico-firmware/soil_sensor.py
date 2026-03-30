from machine import ADC, Pin

class SoilSensor:

    def __init__(self, pin_number):
        self.adc = ADC(Pin(pin_number))

    def read(self):
        return self.adc.read_u16()