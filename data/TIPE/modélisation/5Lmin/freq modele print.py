import csv
import os
import inspect

from detecta import detect_peaks

##Débit moyen
file=open('C:\\Users\\Louis\\Documents\\TIPE\\modélisation2\\5Lmin\\signal.txt', 'r')
reader = csv.reader(file,delimiter='\t',skipinitialspace=True)

X = []
Y = []
A = []

for row in reader:
    X.append(float(row[0])) # les virgules sont remplacées par des points
    Y.append(float(row[1]))

moy = 0

for u in range(len(Y)-1):
    A.append((Y[u]+Y[u+1])/2*(X[u+1]-X[u]))

for p in range(len(A)):
    moy = moy + A[p]
moy = moy/1000

##max min
file2=open('C:\\Users\\Louis\\Documents\\TIPE\\modélisation2\\5Lmin\\pression_model.txt', 'r')
reader = csv.reader(file2,delimiter=',',skipinitialspace=True)

XP = []
YP = []

for row in reader:
    XP.append(float(row[0])) # les virgules sont remplacées par des points
    YP.append(float(row[1]))

maxP = max(YP)
minP = min(YP[XP.index(5):]) #va chercher la valeur min dans YP a partir de la valeur XP[i] = 5 jusqu'à la fin de la liste

DP = maxP-minP

##détection fréquence cardique
i = XP.index(int(3))
YPFC = YP[i:]
XPFC = XP[i:]

pic = detect_peaks(YPFC)

picok = []
m = len(pic)

for l in range(m):
    if pic[l]>maxP - 5:
        picok.append(pic[l])


DT = XPFC[picok[-1]]-XPFC[picok[0]]

FC = (len(picok)-1)*60/DT

print("Débit cardiaque:",  moy, "L/min \n Delta préssion", DP, "mmHg \n Pression max", maxP ,"mmHg \n Pression min", minP, "mmHg \n Fréquence cardiaque", FC, "bat/min")