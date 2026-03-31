from machine import Pin, ADC
import time
from soil_sensor import SoilSensor


SENSOR_ADC = 26
SENSOR_POWER = 15

sensor = SoilSensor(SENSOR_ADC, SENSOR_POWER)

test = ADC(Pin(SENSOR_ADC))


while True:
    sensor.power_on()
    print("sensor is on...")
    
    raw = test.read_u16()
    print("Raw value: ", raw)

    # print("Percentage value: ", percent)

    sensor.power_off()
    print("power is off...")
    time.sleep(5)






