### lib thermomètre
import os
import csv
import time

### lib débitmètre
import RPi.GPIO as GPIO
import time, sys

### lib manomètre
import Adafruit_ADS1x15



### thermomètre init
file=open('/home/pi/Desktop/TIPE/capteurs/valeurs/thermometre_valeur.txt', 'r')

### graph init
file2=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'a')
file2.truncate(0)
file2.close

### débitmètre init
# Initialisation des GPIO
FLOW_SENSOR_GPIO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0

### manomètre init
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

### valeur init
Time = [0]
Debit = [0]
Pres = [0]
Temp = []

global time_init
time_init = time.time()

rang = 0

#thempérature t0
Temp.append(file.readlines()[-1])

#manomètre t0
value = adc.read_adc(0, gain=2/3)  # Lecture du port A0 de la carte ADC1115 || Gain obtenu par lecture du dossier technique
volts = value / 32767 * 6.144 # Ratio of 15 bit value to max volts determines volts
#pa = 2500 * (volts - 0.1015) + 0.5 # Formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration || valeur obtenue en hPa
bar = (2500 * (volts - 0.1015) + 0.5)/1000 # Formule obtenue lecture du datasheet et offset (-0.1015) par test pour la calibration || valeur obtenue en bar
Pres_init = round(bar*750,3) #passage de bar à mmHg

def countPulse(channel):
    global time_init
    Time.append(time.time()-time_init)

    #compte pulse débitmètre
    global count
    if start_counter == 1:
        count = count+1

    #Récup température
    file=open('/home/pi/Desktop/TIPE/capteurs/valeurs/thermometre_valeur.txt', 'r')
    Temp.append(file.readlines()[-1]) #récupération de la dernière valeur du thermomètre
    file.close()

    #Récup manomètre
    value = adc.read_adc(0, gain=2/3)
    volts = value / 32767 * 6.144
    bar = (2500 * (volts - 0.1015) + 0.5)/1000
    Pres.append(round((bar*750) - Pres_init,3))
    Debit.append(Debit[-1])


GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)

while True:
    try:
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        flow = count / 7.5
        debit = 1.927*flow-2.156 #formule obtenue par régression
        if debit<=0:
            Debit.append(0)
        else:
            Debit.append(debit)
        count = 0

        fin = min(len(Time), len(Pres), len(Temp), len(Debit))

        file2=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'a')
        #passage au string parce que les floats ne sont pas "subscriptable"
        for i in range(rang, fin):
            file2.write(f"{str(Time[i])}\t {str(Debit[i])}\t {str(Pres[i])}\t {str(Temp[i])}")
        file2.close

        rang = fin

    except KeyboardInterrupt:
        print('\nkeyboard interrupt!') #Ctrl + C
        GPIO.cleanup()
        sys.exit()