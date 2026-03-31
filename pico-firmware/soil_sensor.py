from machine import ADC, Pin
import time


class SoilSensor:
    def __init__(self, adc_pin_number, power_pin_number, dry_raw=50000, wet_raw=20000):
        self.adc = ADC(Pin(adc_pin_number))
        self.power = Pin(power_pin_number, Pin.OUT, value=0)
        self.dry_raw = dry_raw
        self.wet_raw = wet_raw

    def _to_percent(self, raw):
        span = self.dry_raw - self.wet_raw
        if span == 0:
            return 0
        percent = int((self.dry_raw - raw) * 100 / span)
        return max(0, min(100, percent))

    def read(self, samples=6, gap_ms=2):
        total = 0
        for _ in range(samples):
            total += self.adc.read_u16()
            time.sleep_ms(gap_ms)
        raw = total // samples
        percent = self._to_percent(raw)
        return raw, percent

    def power_on(self, settle_ms=80):
        self.power.value(1)
        time.sleep_ms(settle_ms)

    def power_off(self):
        self.power.value(0)