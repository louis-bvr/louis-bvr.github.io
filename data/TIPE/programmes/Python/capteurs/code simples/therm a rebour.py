import os
import csv
import time

data=open('/home/pi/Desktop/TIPE/capteurs/thermomètre/thermometre_valeur.txt', 'r')
reader = csv.reader(data,delimiter='\t',skipinitialspace=True)
Temptxt =[]

for row in reader:
    Temptxt.append(str(row[0]))
Temp.append(float(Temptxt[-1]))