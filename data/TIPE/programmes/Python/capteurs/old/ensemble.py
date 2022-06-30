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
calibrationFactor = 7.5
time_start= time.time()    # en secondes

### thermomètre init
import glob
Pin_thermomètre = 17
GPIO.setup(Pin_thermomètre, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

### manomètre init
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# Gain = 2/3 for reading voltages from 0 to 6.144V.
# See table 3 in ADS1115 datasheet
GAIN = 2/3

### thermomètre code
def lire_fichier (emplacement) :
    # Ouverture du fichier contenant la temperature
    fichier = open(emplacement)
    # Lecture du fichier
    contenu = fichier.read()
    # Fermeture du fichier apres qu'il ai ete lu
    fichier.close()
    return contenu


def extraire_temperature (contenu) :
    # Supprimer la premiere ligne qui est inutile
    seconde_ligne = contenu.split("\n")[1]
    donnees_temperature = seconde_ligne.split(" ")[9]
    # Supprimer le "t=", et ajouter une virgule
    return float(donnees_temperature[2:]) / 1000


# Recuperation des fichiers contenant la temperature
routes_capteurs = glob.glob("/sys/bus/w1/devices/28*/w1_slave")


def fct_decompte(channel):
### récuperation débitmètre
    global pulseCount
    global time_start
    pulseCount += 1

    # Enregistrement des donnees toutes les 1 secondes
    tdelta = (time.time() - time_start)
    if tdelta  >= 1:
        # Calcul du flux
        flow = (pulseCount / calibrationFactor) / (tdelta * 60)
        flow = round(flow,2)


### récuperation Manomètre
        value = adc.read_adc(0, gain=GAIN)# Lecture du port A0 de la carte ADC1115
        volts = value / 32767.0 * 6.144 # Ratio of 15 bit value to max volts determines volts
        pa = 2500 * (volts - 0.1015) + 0.5 #formule obtenu lecture du datasheet et offset (-0.1015) par test pour la calibration


### récuperation Thermomètre
        if len(routes_capteurs) > 0 :
            contenu_fichier = lire_fichier(routes_capteurs[0])
            temperature = extraire_temperature(contenu_fichier)
            #print ("Température :", temperature, "°C \n")

        else :
            print("Sonde non détectee. Vérifier le branchement, ou rendez-vous dans la section montrant une solution possible")

        print (time.asctime( time.localtime(time.time()) ),' debit : ', flow, 'l/min ')
        print("Pression:", pa, "hpa \t || \t", pa/1000, "bar")
        #print("Tension manomètre", volts, "volt")
        print ("Température :", temperature, "°C \n")

        # Remise à zéro
        tdelta = 0
        pulseCount = 0
        time_start = time.time()

GPIO.add_event_detect(Pin_thermomètre, GPIO.RISING, callback=fct_decompte) #lance le code si un evenelent en detecter que la Pin GPIO17(=Pin_FlowSensor)


