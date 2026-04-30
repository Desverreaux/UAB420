'''
Functions to take readings from the moisture sensor and convert them from
analog values into percentage values.
'''

from machine import ADC
import time


ADC_PIN = 26


_adc = ADC(ADC_PIN)


def _read_raw(n_samples=5):
    '''
    Reads a given number of samples from the moisture sensor and takes the average.
    Returns the average.
    '''
    total = 0
    for _ in range(n_samples):
        total += _adc.read_u16()
        time.sleep_ms(10)
    return total // n_samples


def raw_to_pct(raw, dry_raw, wet_raw):
    '''
    Takes a raw value reading and dry_raw and wet_raw calibration values.
    and returns a value as a float from 0 to 1 as expected by the API.
    If the value ever ends up outside that range, it simply returns 0 or 1.
    '''
    value = (dry_raw - raw) / (dry_raw - wet_raw)
    if (value > 1):
        return 1.0
    elif (value < 0):
        return 0.0
    else:
        return value

def read(cfg):
    '''
    Takes a moisture reading. 
    Takes calibration values from the config file (dry_raw and wet_raw, being the readings for most dry and most wet respectively)
    and readings from the sensor to return both the raw reading and a moisture percentage.
    '''
    dry_raw = cfg["sensor"]["calibration"]["dry_raw"]
    wet_raw = cfg["sensor"]["calibration"]["wet_raw"]


    raw = _read_raw(n_samples=5)
    pct = raw_to_pct(raw, dry_raw, wet_raw)

    return {
        "raw_adc": raw,
        "moisture_pct": pct
    }
