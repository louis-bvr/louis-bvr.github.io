### lib thermomètre
from ftplib import parse150
import os
import csv
import time

### lib débitmètre
import RPi.GPIO as GPIO
import time, sys

### lib manomètre
import Adafruit_ADS1x15

### thermomètre init
data=open('/home/pi/Desktop/TIPE/capteurs/valeurs/thermometre_valeur.txt', 'r')
reader = csv.reader(data,delimiter='\n',skipinitialspace=True)
Temptxt =[]

### graph init
data2=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'a')
data2.truncate(0)
data2.close

### débitmètre init
# Initialisation des GPIO
FLOW_SENSOR_GPIO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0

### manomètre init
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
GAIN = 2/3      #obtenu par lecture du dossier technique

### valeur init
Time = []
Debit = [0]
Pres = []
Temp = [0]

global time_init
time_init = time.time()



#manomètre t0
value = adc.read_adc(0, gain=GAIN)
volts = value / 32767.0 * 6.144
#pa = 2500 * (volts - 0.1015) + 0.5 # Formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration || valeur obtenu en hPa
bar = (2500 * (volts - 0.1015) + 0.5)/1000 # Formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration || valeur obtenu en bar
Pres_init = round(bar*750,3) #passage de bar a mmHg

def countPulse(channel):
    global time_init
    Time.append(time.time()-time_init)

    #compte pulse débitmètre
    global count
    if start_counter == 1:
        count = count+1

    #Récup température

    for row in reader:
        Temptxt.append(float(row[0]))
    #print(Temptxt)
    Temp.append(Temptxt[-1])

    #Récup manomètre
    value = adc.read_adc(0, gain=GAIN)      # Lecture du port A0 de la carte ADC1115
    volts = value / 32767.0 * 6.144         # Ratio of 15 bit value to max volts determines volts
    bar = (2500 * (volts - 0.1015) + 0.5)/1000      # Formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration || valeur obtenu en bar
    Pres.append(round((bar*750) - Pres_init,3))

    #Affichage Valeur
    print("Temps :", Time[-1] ,"sec")
    print ("Débit :", Debit[-1], "l/min ") #10% erreur
    print("Pression:", (Pres[-1]*750), "bar || ", Pres[-1], "mmHg") #5% erreur
    print ("Température :", Temp[-1], "°C +/- 0,5°C \n") #erreur = 0,5°C


    data2=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'a')

    #passage au string parce que les floats ne sont pas "subscriptable"
    data2.write(f"{str(Time[-1])}\t {str(Debit[-1])}\t {str(Pres[-1])}\t {str(Temp[-1])}\n")

    data2.close

GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)

while True:
    try:
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        Debit.append(count / 7.5)
        #print("Débit:", flow, "L/min")
        count = 0

    except KeyboardInterrupt:
        print('\nkeyboard interrupt!') #Ctrl + C
        GPIO.cleanup()
        sys.exit()
"""
    #enregistrement
    time1 = str(Time[-1])
    flow1 = str(Debit[-1])
    pres1 = str(Pres[-1])
    temp1 = str(Temp[-1])
"""

"""
V1 : compilation des capteurs
V2 : Graphique dynamique
V2.5 : Multi Graphique dynamique
V3 : opti thermomètre
V4 : opti
V4.5 : incertitude
V5 : séparation capteur/graph
V10 : réécriture
V11 : incertitude (ou direct depuis le graph ?)

V... : détection max, détection fréquence, calculs, détermination pb
"""