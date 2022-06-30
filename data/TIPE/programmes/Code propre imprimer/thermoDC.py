import matplotlib.pyplot as plt
import math as m
import csv
import os
import inspect


file2=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'r')
reader = csv.reader(file2,delimiter='\t',skipinitialspace=True)

Temps=[]
Valeur=[]

for row in reader:
    Temps.append(float(row[0])) #récupère la valeur Time du fichier valeurs.txt
    Valeur.append(float(row[2])) #récupère la valeur Temps du fichier valeurs.txt

Tinit = Valeur[0]
Valeurinv = []

for i in range(len(Valeur)):
    Valeurinv.append(-(Valeur[i]-Tinit))

Valeurinvfiltre = []
Tempsfiltre = []
J = []

for j in range(len(Valeurinv)):
    if Valeurinv[j]>max(Valeurinv)*0.05:
        Valeurinvfiltre.append(Valeurinv[j])
        Tempsfiltre.append(Temps[j])
        J.append(j)

Valeurinvfiltre.insert(0,Valeurinv[J[0]-1])
Tempsfiltre.insert(0,Temps[J[0]-1])

A = []
moy = 0

for u in range(len(Tempsfiltre)-1):
    A.append((Valeurinvfiltre[u]+Valeurinvfiltre[u+1])/2*(Tempsfiltre[u+1]-Tempsfiltre[u]))

air = 0
for p in range(len(A)):
    air = air + A[p]

def DC(Ti, Vi):
    DC = ((Tinit-Ti)*Vi*0.00238)/air
    incert = m.sqrt(abs(Vi*0.00238/air)**2*(0.5**2))

    print("Débit cardiaque :", round(DC,7), "+/-", round(incert, 6), "m3/sec")
    print("Débit cardiaque :", round(DC*60000,3), "+/-", round(incert*60000, 3), "L/min")
