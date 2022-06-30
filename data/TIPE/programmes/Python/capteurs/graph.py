### lib graphique
import matplotlib.pyplot as plt

import random as rd

import os
import csv
import time

#data=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'r')
data=open('C:\\Users\\Louis\\Desktop\\TIPE\\capteurs\\valeurs\\valeurs.txt', 'r')
reader = csv.reader(data,delimiter='\t',skipinitialspace=True)



Time = []
Temp = []
Debit = []
Pres = []

for row in reader:
    Time.append(float(row[0]))
    Debit.append(float(row[1]))
    Pres.append(float(row[2]))
    Temp.append(float(row[3]))

plt.ion()

figure, ax = plt.subplots()
line1, = ax.plot(Time, Temp, label="Température (°C)")
line2, = ax.plot(Time, Debit, label="Débit (L/min)")
line3, = ax.plot(Time, Pres, label="Pression (mmHg)")


while True:
    Time = []
    Temp = []
    Debit = []
    Pres = []

    for row in reader:
        Time.append(float(row[0]))
        Debit.append(float(row[1]))
        Pres.append(float(row[2]))
        Temp.append(float(row[3]))


    line1.set_data(Time, Temp)
    line2.set_data(Time, Debit)
    line3.set_data(Time, Pres)

    plt.xlabel("Temps")
    plt.ylabel("Données")
    plt.legend()



    plt.axis([0, Time[-1]+1, min(min(Temp), min(Debit), min(Pres)) , max(max(Temp), max(Debit), max(Pres)) + 10])

    figure.canvas.draw()
    figure.canvas.flush_events()

