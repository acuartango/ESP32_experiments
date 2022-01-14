# This is your main script.
##from machine import Pin, ADC
##from time import sleep

##pot = ADC(0) # En ESP8266 Pin "A0"
#pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v

#pin = Pin(16, Pin.OUT, Pin.PULL_UP)

##pin = Pin(5, Pin.OUT) # En ESP8266 Pin "D2"
##pin.value(1)


##while True:
##  pot_value = pot.read()
##  print(pot_value)
##  sleep(1)


print("\nHola mundo\n")

import utime
from machine import Pin, I2C

import ahtx0

# I2C for the Wemos D1 Mini with ESP8266
i2c = I2C(scl=Pin(5), sda=Pin(4))

# Create the sensor object using I2C
sensor = ahtx0.AHT10(i2c)

while True:
    print("\nTemperature: %0.2f C" % sensor.temperature)
    print("Humidity: %0.2f %%" % sensor.relative_humidity)
    Pin(2, Pin.OUT).on()
    utime.sleep(5)
    Pin(2, Pin.OUT).off()
