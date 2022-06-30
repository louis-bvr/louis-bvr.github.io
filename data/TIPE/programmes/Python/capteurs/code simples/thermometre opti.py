import glob
routes_capteurs = glob.glob("/sys/bus/w1/devices/28*/w1_slave")
fichier = open(routes_capteurs[0])

import time

time_init = time.time()

def extraire_temperature () :
    contenu = fichier.read()
    # Supprimer la premiere ligne qui est inutile
    seconde_ligne = contenu.split("\n")[1]
    donnees_temperature = seconde_ligne.split(" ")[9]
    # Supprimer le "t=", et ajouter une virgule
    return float(donnees_temperature[2:]) / 1000



temperature = extraire_temperature()
print ("Temperature :", temperature)
print("temps:", round(time.time() - time_init, 3))
