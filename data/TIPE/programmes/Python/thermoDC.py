import matplotlib.pyplot as plt
import math as m
import csv
import os
import inspect


file2=open('C:\\Users\\Louis\\Desktop\\t2.txt', 'r')
reader = csv.reader(file2,delimiter='\t',skipinitialspace=True)

Temps=[]
Valeur=[]

for row in reader:
    Temps.append(float(row[0])) #récupère la valeur Time du fichier valeurs.txt
    Valeur.append(float(row[1])) #récupère la valeur Temps du fichier valeurs.txt

#print(Temps)
#print(Valeur)

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

#print(air)

#DC = ((Ts-Ti)*Vi*K)/air
DC = ((26.56-6.68)*0.02*(2.28*10**-3))/air
#DC = ((27.25-7.86)*0.02*(2.28*10**-3))/air

#print (air)

incert = m.sqrt(abs(0.02*0.00238/air)**2*(0.5**2))

print("Débit cardiaque :", round(DC,7), "+/-", round(incert, 6), "m3/sec")
print("Débit cardiaque :", round(DC*60000,3), "+/-", round(incert*60000, 3), "L/min")


#plt.plot(Temps, Valeur)
plt.plot(Temps, Valeurinv)
#plt.plot(Tempsfiltre, Valeurinvfiltre)
plt.show()
