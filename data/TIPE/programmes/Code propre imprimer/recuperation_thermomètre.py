import glob
routes_capteurs = glob.glob("/sys/bus/w1/devices/28*/w1_slave")



data=open('/home/pi/Desktop/TIPE/capteurs/valeurs/thermometre_valeur.txt', 'a')
data.truncate(0)
data.close()


def extraire_temperature () :
    contenu = fichier.read()
    # Supprimer la premiere ligne qui est inutile
    seconde_ligne = contenu.split("\n")[1]
    donnees_temperature = seconde_ligne.split(" ")[9]
    # Supprimer le "t=", et ajouter une virgule
    return float(donnees_temperature[2:]) / 1000

while True:
    data=open('/home/pi/Desktop/TIPE/capteurs/valeurs/thermometre_valeur.txt', 'a')
    fichier = open(routes_capteurs[0])
    temperature = extraire_temperature()
    data.write(f"{temperature}\n")
    print("temp capt", temperature)
    fichier.close()