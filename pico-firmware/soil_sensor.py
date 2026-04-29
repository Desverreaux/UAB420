from machine import ADC
import time


ADC_PIN = 26


_adc = ADC(ADC_PIN)


def _read_raw(n_samples=5):
    total = 0
    for _ in range(n_samples):
        total += _adc.read_u16()
        time.sleep_ms(10)
    return total // n_samples


def raw_to_pct(raw, dry_raw, wet_raw):
    value = (dry_raw - raw) / (dry_raw - wet_raw)
    if (value > 1):
        return 1.0
    elif (value < 0):
        return 0.0
    else:
        return value

def read(cfg):
    dry_raw = cfg["sensor"]["calibration"]["dry_raw"]
    wet_raw = cfg["sensor"]["calibration"]["wet_raw"]


    raw = _read_raw(n_samples=5)
    pct = raw_to_pct(raw, dry_raw, wet_raw)

    return {
        "raw_adc": raw,
        "moisture_pct": pct
    }
