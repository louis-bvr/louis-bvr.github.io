
import numpy as np
import time
import matplotlib.pyplot as plt

X = [0]
Y = [0]
YI = [0]

plt.ion()

figure, ax = plt.subplots()
line1, = ax.plot(X, Y)
line2, = ax.plot(X, YI)

for p in range(100):
    X.append(X[-1]+1)
    Y.append(X[-1]**2)
    YI.append(X[-1]**2 +1)

    print(X)
    print(Y)
    print(YI)


    line1.set_xdata(X)
    line1.set_ydata(Y)
    line2.set_xdata(X)
    line2.set_ydata(YI)

    plt.axis([0, X[-1],-10, Y[-1]])

    figure.canvas.draw()

    figure.canvas.flush_events()

    time.sleep(1)

"""
import numpy as np
import time
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = np.cos(x)
yi = np.sin(x)

plt.ion()

figure, ax = plt.subplots()
line1, = ax.plot(x, y)
line2, = ax.plot(x, yi)

plt.title("Dynamic Plot of sinx",fontsize=25)

plt.xlabel("X",fontsize=18)
plt.ylabel("sinX",fontsize=18)

for p in range(100):
    updated_y = np.cos(x-0.05*p)
    updated_yi = np.sin(x-0.05*p)

    line1.set_xdata(x)
    line1.set_ydata(updated_y)
    line2.set_ydata(updated_yi)

    figure.canvas.draw()

    figure.canvas.flush_events()
    time.sleep(0.5)
"""

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = [0]
y = [0]
p = 0

figure, ax = plt.subplots()
line, = ax.plot(x, y)

def func_animate(i):
    x.append(x[-1]+1)
    y.append(x[-1]**2)
    plt.axis([0, x[-1],0, y[-1]])

    line.set_data(x, y)

    return line,

ani = FuncAnimation(figure,func_animate)


plt.show()
"""

