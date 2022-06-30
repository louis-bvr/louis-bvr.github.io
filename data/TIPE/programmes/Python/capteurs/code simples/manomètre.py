from time import sleep

import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# Gain = 2/3 for reading voltages from 0 to 6.144V.
# See table 3 in ADS1115 datasheet
GAIN = 2/3
offset = 0.08

# Main loop.
while 1:
    # Read ADC channel 0
    value = adc.read_adc(0, gain=GAIN)
    # Ratio of 16 bit value to max volts determines volts
    volts = value / 32768 * 6.144
    # Tests shows linear relationship between psi & voltage:
    pa = 2500 * (volts - 0.1015) + 0.5

    print("tension", volts, "volt")
    print("Pression:", pa, "hpa \t || \t", pa/1000, "bar \n")

    """
    psi = 50.0 * volts - 10.8
    # Bar conversion
    bar = psi * 0.0689475729

    print("pression:", bar, "bar")
    print("tension", volts, "volt \n")
"""