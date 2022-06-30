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
data=open('/home/pi/Desktop/TIPE/capteurs/thermomètre/thermometre_valeur.txt', 'r')
reader = csv.reader(data,delimiter='\t',skipinitialspace=True)
Temptxt =[]

### graph init
data2=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'a')

### débitmètre init
# Initialisation des GPIO
Pin_FlowSensor = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Pin_FlowSensor, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

pulseCount = 0
global tdelta
tdelta = 0
calibrationFactor = 7.5     #obtenu par lecture du dossier technique
global flow
flow = 0
time_start= time.time()     #en secondes

### manomètre init

adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

GAIN = 2/3      #obtenu par lecture du dossier technique

### initialisation valeur
Time = [0]
Temp = []
Debit = [0]
Pres = []

#thermomètre
for row in reader:
    Temptxt.append(str(row[0]))
Temp.append(float(Temptxt[-1]))

#manomètre
value = adc.read_adc(0, gain=GAIN)
volts = value / 32767.0 * 6.144
pa = 2500 * (volts - 0.1015) + 0.5 # Formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration
global Pres_init
Pres_init = round((pa/1000)*750,3) #passage de Pascal a mmHg

time_init = time.time()

def fct_decompte(channel, blit = True):
### récuperation débitmètre
    global pulseCount
    global time_start
    global flow
    global Pres_init
    pulseCount += 1

    # Enregistrement des donnees toutes les 1 secondes
    tdelta = (time.time() - time_start)

    if tdelta  >= 0.2:
        flow = round((pulseCount / calibrationFactor) / (tdelta * 60),3)    # Calcul du débit volumique
        eflow = flow*0.005 #erreur = 0,5%
        Debit.append(flow)

        # Remise à zéro
        tdelta = 0
        pulseCount = 0
        time_start = time.time()

### récuperation Manomètre
    value = adc.read_adc(0, gain=GAIN)      # Lecture du port A0 de la carte ADC1115
    volts = value / 32767.0 * 6.144         # Ratio of 15 bit value to max volts determines volts
    pa = 2500 * (volts - 0.1015) + 0.5      # Formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration
    epa = pa*0.5/100 #erreur = 5%

### récuperation Thermomètre

    for row in reader:
        Temptxt.append(str(row[0]))
    Temp.append(float(Temptxt[-1]))
    #revoir cette parti

### affichage/collecte valeur
    time_tot = time.time() - time_init

    Time.append(time_tot)
    Pres.append(round(Pres_init-(pa/1000)*750,3))

    print("Temps :", round(time_tot,2) ,"sec" )
    print ("Débit :", flow, 'l/min +/-', eflow)
    print("Pression:", Pres[-1]/750, "bar +/-", epa,  "||   ", Pres[-1], "mmHg, +/-", (epa/1000)*750)
    print ("Température :", Temp[-1], "°C +/- 0,5°C \n") #erreur = 0,5°C

    data2.write(f"{Time[-1]}\t {flow[-1]}\t {Pres[-1]}\t {Temp[-1]}\n")



GPIO.add_event_detect(Pin_FlowSensor, GPIO.RISING, callback=fct_decompte)   #lance le code si un évènement est détecté sur la broche GPIO_17 (=Pin_FlowSensor)





"""
V1 : compilation des capteurs
V2 : Graphique dynamique
V2.5 : Multi Graphique dynamique
V3 : opti thermomètre
V4 : opti
V4.5 : incertitude
V5 : séparation capteur/graph

V... : détection max, détection fréquence, calculs, détermination pb
"""