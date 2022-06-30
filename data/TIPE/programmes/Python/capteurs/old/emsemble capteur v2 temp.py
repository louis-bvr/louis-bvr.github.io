### thermomètre init
import glob


### débitmètre init
# Initialisation des GPIO
import RPi.GPIO as GPIO
import time, sys
Pin_FlowSensor = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Pin_FlowSensor, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

pulseCount = 0
global tdelta
tdelta = 0
calibrationFactor = 7.5     #obtenu par lecture du dossier technique
time_start= time.time()     #en secondes


### manomètre init
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

GAIN = 2/3      #obtenu par lecture du dossier technique


### Parti graphique
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
time_init = time.time()
Time = [0]
#Temp = [0]
Debit = [0]
Pres = [0]

"""
### thermomètre code
def lire_fichier (emplacement):
    fichier = open(emplacement)     # Ouverture du fichier contenant la temperature
    contenu = fichier.read()    # Lecture du fichier
    fichier.close()     # Fermeture du fichier apres qu'il ai ete lu
    return contenu


def extraire_temperature (contenu):
    seconde_ligne = contenu.split("\n")[1]      # Supprimer la premiere ligne qui est inutile
    donnees_temperature = seconde_ligne.split(" ")[9]
    return float(donnees_temperature[2:]) / 1000    # Supprimer le "t=", et ajouter une virgule


routes_capteurs = glob.glob("/sys/bus/w1/devices/28*/w1_slave")     # Recuperation des fichiers contenant la temperature
"""

def fct_decompte(channel):
### récuperation débitmètre
    global pulseCount
    global time_start
    pulseCount += 1

    # Enregistrement des donnees toutes les 1 secondes
    tdelta = (time.time() - time_start)
    if tdelta  >= 1:
        flow = round((pulseCount / calibrationFactor) / (tdelta * 60),3)    # Calcul du débit volumique

### récuperation Manomètre
        value = adc.read_adc(0, gain=GAIN)      # Lecture du port A0 de la carte ADC1115
        volts = value / 32767.0 * 6.144         # Ratio of 15 bit value to max volts determines volts
        pa = 2500 * (volts - 0.1015) + 0.5      # Formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration


### récuperation Thermomètre
        #contenu_fichier = lire_fichier(routes_capteurs[0])
        #temperature = extraire_temperature(contenu_fichier)


### affichage
        time_tot = time.time() - time_init

        Time.append(time_tot)
        #Temp.append(temperature)
        Debit.append(flow)
        Pres.append((pa/1000)*750)

        print("Temps :", round(time_tot,1) ,"sec" )
        print ("Débit :", flow, 'l/min ')
        print("Pression:", round(pa/1000, 3), "bar   ||   ", round((pa/1000)*750,3), "mmHg")
        #print ("Température :", round(temperature,3), "°C \n")


### graphique dynamique

        plt.ion()

        figure, ax = plt.subplots()
        #line1, = ax.plot(Temps, Temp, label="Température (°C)")
        line2, = ax.plot(Temps, Debit, label="Débit (L/min)")
        line3, = ax.plot(Temps, Pres, label="Pression (mmHg)")

        line1.set_xdata(Time)
        #line1.set_ydata(Temp)
        line2.set_ydata(Debit)
        line3.set_ydata(Pres)

        plt.axis([0, x[-1]+1, min(Debit, Pres), max(Debit, Pres)])

        figure.canvas.draw()
        figure.canvas.flush_events()

        plt.xlabel("Temps")
        plt.legend()

        # Remise à zéro
        tdelta = 0
        pulseCount = 0
        time_start = time.time()



GPIO.add_event_detect(Pin_FlowSensor, GPIO.RISING, callback=fct_decompte)   #lance le code si un évènement est détecté sur la broche GPIO_17 (=Pin_FlowSensor)











"""
V1 : compilation des capteurs
V2 : Graphique dynamique
"""