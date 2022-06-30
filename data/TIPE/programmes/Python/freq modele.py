import csv
import os
import inspect

from detecta import detect_peaks

##Débit moyen
file=open('C:\\Users\\Louis\\Documents\\TIPE\\Python\\capteurs\\valeurs\\valeurs1.txt', 'r')
reader = csv.reader(file,delimiter='\t',skipinitialspace=True)

Time = []
Debit = []
Press = []
Temp = []

Debitmoy = []


for row in reader:
    Time.append(float(row[0]))
    Debit.append(float(row[1]))
    Press.append(float(row[2]))
    Temp.append(float(row[3]))
    print(Temps)

moy = 0

for u in range(len(Debit)-1):
    Debitmoy.append((Debit[u]+Debit[u+1])/2*(Time[u+1]-Time[u]))

for p in range(len(Debitmoy)):
    moy = moy + Debitmoy[p]

##max min



maxP = max(Press)
minP = min(Press[Time.index(2):]) #va chercher la valeur min dans YP a partir de la valeur XP[i] = 5 jusqu'à la fin de la liste

DP = maxP-minP

##tau
tau = 1.2* (DP/(moy*14.815)) #1.2 = C = compliance moyenne retenue, R = DP/qv (PA = Qc. RAS ou PA = VES.FC.RAS, résistances artérielles systémiques (RAS)) | *14.815 : passage L/min to cm3/Sec


##détection fréquence cardique
i = Time.index(int(3*tau))
PressFC = Press[i:]
TimeFC = Time[i:]

pic = detect_peaks(PressFC)

picok = []
m = len(pic)

for l in range(m):
    if pic[l]>maxP - 5:
        picok.append(pic[l])


DT = TimeFC[picok[-1]]-TimeFC[picok[0]]

FC = (len(picok)-1)*60/DT

print("Débit cardiaque:",  moy, "L/min \n Delta préssion", DP, "mmHg \n Pression max", maxP ,"mmHg \n Pression min", minP, "mmHg \n tau", tau, "sec \n Fréquence cardiaque", FC, "bat/min")







def DB():
    file=open('C:\\Users\\Louis\\Documents\\TIPE\\modélisation\\modele these\\signal.txt', 'r')
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
    #print("Débit cardiaque:",  moy/1000, "L/min")
    return "Débit cardiaque:",  moy/1000, "L/min"

def maxmin():
    file2=open('C:\\Users\\Louis\\Documents\\TIPE\\modélisation\\modele these\\pression_model.txt', 'r')
    reader = csv.reader(file2,delimiter=',',skipinitialspace=True)

    XP = []
    YP = []

    for row in reader:
        X.append(float(row[0])) # les virgules sont remplacées par des points
        Y.append(float(row[1]))

    maxP = max(Y)
    minP = min(Y[X.index(5):]) #va chercher la valeur min dans Y a partir de la valeur X[i] = 5 jusqu'à la fin de la liste

    DP = maxP-minP

    return "DP", DP, "| MaxP", maxP ,"| MinP", minP


def detectionPics () :
    file2=open('C:\\Users\\Louis\\Documents\\TIPE\\modélisation\\modele these\\pression_model.txt', 'r')
    reader = csv.reader(file2,delimiter=',',skipinitialspace=True)

    tau = 0.6991849686108549

    XP = []
    YP = []

    for row in reader:
        XP.append(float(row[0])) # les virgules sont remplacées par des points
        YP.append(float(row[1]))

    i = XP.index(int(3*tau))
    YPFC = YP[i:]
    XPFC = XP[i:]
    #print(YPFC)




    index = detect_peaks(YPFC)

    DT = XPFC[index[-1]]-XPFC[index[0]]
    for i in range(len(index)):
        print(XPFC[index[i]])
    #print(i)
    print(index)
    print(DT)

    FC = (len(index)-1)*60/DT

    print(FC)








"""
def pulsationCardiaque (signal , Te , seuil) :
    pics = [ ]
    deb = 0
    nbPoints = int ( 3 / Te )
    while deb+nbPoints < len ( signal ):
        deb = deb+detectionPics ( signal [ deb : deb+nbPoints ] , seuil )
        pics . append ( deb )
        periode_moy = ( pics[−1]− pics [0]) *Te / ( len ( pics ) −1)
    return 60 / periode_moy
"""