import matplotlib.pyplot as plt
import math as m
import csv
import os
import inspect

from detecta import detect_peaks

file2=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'r')
reader = csv.reader(file2,delimiter='\t',skipinitialspace=True)

Temps = []
Valeur = []


A = []

for row in reader:
    Temps.append(float(row[0])) #récupère la valeur Time du fichier valeurs.txt
    Valeur.append(float(row[2])) #récupère la valeur Pres du fichier valeurs.txt

## min max pression
maxP = max(Valeur)
minP = min(Valeur[Temps.index(3):]) #va chercher la valeur min dans Valeur a partir de la valeur Temps[i] = 5 jusqu'à la fin de la liste

DP = maxP-minP

## calcul de la fréquence cardiaque
pic = detect_peaks(Valeur)

picnonnp = []
for i in range(len(pic)):
    picnonnp.append(pic[i])

picok = []

for l in range(len(picnonnp)):
    if Valeur[picnonnp[l]]>maxP - 10:
        picok.append(pic[l])

DT = Temps[picok[-1]]-Temps[picok[0]]
FC = (len(picok)-1)*60/DT
print("fréquence cardiaque", round(FC, 3), "battements/min")



### calcul écart type

#calculer du nombre de point par période
nbpoint = len(Valeur)//len(picok)


P1 = []
for i in range(2*nbpoint,3*nbpoint):
    P1.append(Valeur[i])

P2 = []
for i in range(3*nbpoint,4*nbpoint):
    P2.append(Valeur[i])

P3 = []
for i in range(4*nbpoint,5*nbpoint):
    P3.append(Valeur[i])

SP1 = 0
for i in range(len(P1)):
    SP1 = SP1 + P1[i]
moyP1 = SP1/len(P1)


PreS1 = []
S1 = 0
for i in range(len(P1)):
    PreS1.append(abs(P1[i]-moyP1)**2)
    S1 = S1 + PreS1[i]

SP2 = 0
for i in range(len(P2)):
    SP2 = SP2 + P2[i]
moyP2 = SP2/len(P2)


PreS2 = []
S2 = 0
for i in range(len(P2)):
    PreS2.append(abs(P2[i]-moyP2)**2)
    S2 = S2 + PreS2[i]

SP3 = 0
for i in range(len(P3)):
    SP3 = SP3 + P3[i]
moyP3 = SP3/len(P3)


PreS3 = []
S3 = 0
for i in range(len(P3)):
    PreS3.append(abs(P3[i]-moyP3)**2)
    S3 = S3 + PreS3[i]


EC1 = m.sqrt(S1/len(P1))
EC2 = m.sqrt(S2/len(P2))
EC3 = m.sqrt(S3/len(P3))

moyEc = (EC1+EC2+EC3)/3

X = -4e-9*moyEc + 1.035e-6 #Formule très simplifier obtenu par le docteur Delphine PLAN

DC = FC * (X*moyEc)

print(round(DC,5),  "+/-", round(DC*0.05, 5),"m3/min")
print(round(DC*1e3, 3), "+/-", round((DC*1e3)*0.05,3), "L/min")