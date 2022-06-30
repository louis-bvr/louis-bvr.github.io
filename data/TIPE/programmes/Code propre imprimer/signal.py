import matplotlib.pyplot as plt
import math as m
import csv
import os
import inspect



def signal(T, Ts, I, s, n):
    dossier=os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
    os.chdir(dossier)

    ##création du signal cardiaque
    p = int(s // T) + 1

    Y = []
    X = []
    rows = []

    L = []

    for l in range(n):
        L.append(l*Ts/n)


    for i in range(n):
        Y.append(I*(m.sin(((m.pi)*L[i])/Ts))**2)
        X.append((i/n)*Ts)


    for j in range(n):
        Y.append(0)
        X.append(Ts+j/n*(T-Ts))

    for w in range(1,p):
        for u in range(2*n):
            Y.append(Y[u])
            X.append(X[u]+(w*T))


    plt.plot(X, Y)
    plt.xlim(0, p*T)
    plt.show()

    data=open('C:\\Users\\Louis\\Documents\\TIPE\\modélisation2\\signal.txt', 'w')
    for o in range(len(Y)):
        data.write(f"{X[o]}\t{Y[o]}\n")
    data.close()


    ##détermination du débit sanguin moyen
    A = []
    moy = 0

    for u in range(len(Y)-1):
        A.append((Y[u]+Y[u+1])/2*(X[u+1]-X[u]))

    for p in range(len(A)):
        moy = moy + A[p]
    print("Débit cardiaque:",  round(moy/1000, 3), "L/min")

#signal(0.8, 0.4, 1000/3, 60, 50)