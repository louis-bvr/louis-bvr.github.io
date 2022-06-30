
### lib graphique
import matplotlib.pyplot as plt

import random as rd

import os
import csv
import time

#data=open('/home/pi/Desktop/TIPE/capteurs/valeurs/valeurs.txt', 'r')
data=open('C:\\Users\\Louis\\Desktop\\TIPE\\capteurs\\valeurs\\valeurs.txt', 'r')
reader = csv.reader(data,delimiter='\n',skipinitialspace=True)



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
    Time.append(Time[-1]+1)
    Temp.append(rd.randint(0,20))
    Debit.append(rd.randint(0,20))
    Pres.append(rd.randint(0,20))


    line1.set_data(Time, Temp)
    line2.set_data(Time, Debit)
    line3.set_data(Time, Pres)

    plt.xlabel("Temps")
    plt.ylabel("Données")
    plt.legend()



    plt.axis([0, Time[-1]+1, min(min(Temp), min(Debit), min(Pres)) , max(max(Temp), max(Debit), max(Pres)) + 10])

    figure.canvas.draw()
    figure.canvas.flush_events()




"""
### lib graphique
import matplotlib.pyplot as plt

import random as rd

import os
import csv
import time


data=open('C:\\Users\\Louis\\Desktop\\TIPE\\capteurs\\valeurs\\valeurs.txt', 'r')
reader = csv.reader(data,delimiter='\t',skipinitialspace=True)

blit = True

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

axbackground = figure.canvas.copy_from_bbox(ax.bbox)

while True:
    Time.append(Time[-1]+1)
    Temp.append(rd.randint(0,20))
    Debit.append(rd.randint(0,20))
    Pres.append(rd.randint(0,20))


    line1.set_data(Time, Temp)
    line2.set_data(Time, Debit)
    line3.set_data(Time, Pres)

    plt.xlabel("Temps")
    plt.ylabel("Données")
    plt.legend()

    figure.canvas.restore_region(axbackground)

    # redraw just the points
    ax.draw_artist(line1)
    ax.draw_artist(line2)
    ax.draw_artist(line3)

    # fill in the axes rectangle
    figure.canvas.blit(ax.bbox)

    plt.axis([0, Time[-1]+1, min(min(Temp), min(Debit), min(Pres)) , max(max(Temp), max(Debit), max(Pres)) + 10])

    figure.canvas.draw()
    figure.canvas.flush_events()
"""