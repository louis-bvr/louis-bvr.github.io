import glob
import time

time_init = time.time()


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


if len(routes_capteurs) > 0 :
    contenu_fichier = lire_fichier(routes_capteurs[0])
    temperature = extraire_temperature(contenu_fichier)
    print ("Temperature :", temperature)
    print("temps:", round(time.time() - time_init, 3))

else :
    print("Sonde non détectee. Vérifier le branchement, ou rendez-vous dans la section montrant une solution possible")


#### FONCTIONNE MAIS A REVOIR POUR SIMPLIFIER ? ####