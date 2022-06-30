from time import sleep

import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# Gain = 2/3 for reading voltages from 0 to 6.144V.
# See table 3 in ADS1115 datasheet
GAIN = 2/3

# Main loop.
while 1:
    value = adc.read_adc(0, gain=GAIN)      # Lecture du port A0 de la carte ADC1115
    volts = value / 32767.0 * 6.144         # Ratio of 15 bit value to max volts determines volts
    bar = (2500 * (volts - 0.1015) + 0.5)/1000      # Formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration || valeur obtenu en bar

    print(bar)
    print(bar*750)

    sleep(1)