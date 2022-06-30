import matplotlib.pyplot as plt
import math as m
import csv
import os
import inspect
from scipy.signal import savgol_filter

file2=open('C:\\Users\\Louis\\Documents\\TIPE\\modélisation2\\chut\\pression_modelok.txt', 'r')
reader = csv.reader(file2,delimiter='\t',skipinitialspace=True)

X = []
Y = []

for row in reader:
    X.append(float(row[0])) # les virgules sont remplacées par des points
    Y.append(float(row[1]))




yhat = savgol_filter(Y, 20, 3)



plt.title("P(t) | P en mmHg ; t en secondes")




data=open('C:\\Users\\Louis\\Documents\\TIPE\\modélisation2\\chut\\pression_modelok.txt', 'a')
data.truncate(0)
for i in range(len(X)):
    data.write(f"{str(X[i])}\t {str(yhat[i])}\n")
data.close

print(len(X), len(Y), len(yhat))

plt.plot(X, Y, label="courbe d'origine")
plt.plot(X,yhat, label="courbe lissée")
plt.legend()
plt.show()
