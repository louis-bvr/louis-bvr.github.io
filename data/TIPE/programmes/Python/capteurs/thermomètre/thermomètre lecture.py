import os
import csv
import time

#reader = csv.reader(data,delimiter='\t',skipinitialspace=True)
data=open('/home/pi/Desktop/TIPE/capteurs/thermomètre/thermometre_valeur.txt', 'r')
reader = csv.reader(data,delimiter='\t',skipinitialspace=True)
Temp = []

#while True:
for row in reader:
    Temp.append(float(row[0]))

print(Temp)
print("Temp, fiche", Temp[-1])


#time.sleep(0.4)