import time
from matplotlib import pyplot as plt
import numpy as np
import random as rd




def live_update_demo(blit = False):
    x = np.linspace(0,50., num=100)
    X,Y = np.meshgrid(x,x)
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    img = ax1.imshow(X, vmin=-1, vmax=1, interpolation="None", cmap="RdBu")

    RD = []

    line, = ax2.plot([], lw=3)
    line2, = ax2
    text = ax2.text(0.8,0.5, "")

    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim([-1.1, 1.1])

    fig.canvas.draw()   # note that the first draw comes before setting data


    if blit:
        # cache the background
        axbackground = fig.canvas.copy_from_bbox(ax1.bbox)
        ax2background = fig.canvas.copy_from_bbox(ax2.bbox)

    plt.show(block=False)


    t_start = time.time()
    k=0.

    for i in np.arange(1000):
        img.set_data(np.sin(X/3.+k)*np.cos(Y/3.+k))
        line.set_data(x, np.sin(x/3.+k))
        tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - t_start)) )
        text.set_text(tx)
        #print tx
        k+=0.11

        if blit:
            # restore background
            fig.canvas.restore_region(axbackground)
            fig.canvas.restore_region(ax2background)

            # redraw just the points
            ax1.draw_artist(img)
            ax2.draw_artist(line)
            ax2.draw_artist(text)

            # fill in the axes rectangle
            fig.canvas.blit(ax1.bbox)
            fig.canvas.blit(ax2.bbox)

            # in this post http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
            # it is mentionned that blit causes strong memory leakage.
            # however, I did not observe that.

        else:
            # redraw everything
            fig.canvas.draw()

        fig.canvas.flush_events()
        #alternatively you could use
        #plt.pause(0.000000000001)
        # however plt.pause calls canvas.draw(), as can be read here:
        #http://bastibe.de/2013-05-30-speeding-up-matplotlib.html



#live_update_demo(False) # 28 fps
live_update_demo(True)   # 175 fps


"""
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget) ## ici

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
"""
"""
import numpy as np
import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtWidgets

app = QtWidgets.QApplication(sys.argv)

x = np.linspace(0, 3.14, 100)
y1 = np.sin(x)#Data number 1 associated to checkbox A1
y2 = np.cos(x)#Data number 2 associated to checkbox A2

curves = [y1, y2]
pens = ["r", "y"]

#This function is called whenever the state of checkboxes changes
def plot_curves(state):
    plot.clear()
    for checkbox, curve, pen in zip(checkboxes, curves, pens):
        if checkbox.isChecked():
            plot.plot(x, curve, pen=pen)

#A widget to hold all of my future widgets
widget_holder = QtWidgets.QWidget()

#Making a pyqtgraph plot widget
plot = pg.PlotWidget()

#Setting the layout
layout = QtWidgets.QGridLayout()
widget_holder.setLayout(layout)

checkboxes = [QtWidgets.QCheckBox() for i in range(2)]
for i, checkbox in enumerate(checkboxes):
    checkbox.setText(f"A{i+1}")
    checkbox.stateChanged.connect(plot_curves)
    layout.addWidget(checkbox, 0, i)

#Adding the widgets to the layout
layout.addWidget(plot, 1, 0, 2, 0)

widget_holder.adjustSize()
widget_holder.show()

sys.exit(app.exec_())
"""


"""

from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget) ## ici

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())

#pip install PyQt5
#pip install pyqtgraph

"""



"""

from PyQt5 import QtWidgets, uic, QtGui
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np
import sys
import string
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

app = QtWidgets.QApplication(sys.argv)

x = np.linspace(0, 3.14, 100)
y1 = np.sin(x)#Data number 1 associated to checkbox A1
y2 = np.cos(x)#Data number 2 associated to checkbox A2

#This function is called whenever the state of checkboxes changes
def todo():
    global b1st, b2st, curve1, curve2
    if cbx1.isChecked() != b1st:
        b1st = cbx1.isChecked()
        if cbx1.isChecked():
            if curve1 is None:
                curve1 = plot.plot(x, y1, pen = 'r')
            else:
                plot.addItem(curve1)
        else:
            plot.removeItem(curve1)

    if cbx2.isChecked() != b2st:
        b2st = cbx2.isChecked()
        if cbx2.isChecked():
            if curve2 is None:
                curve2 = plot.plot(x, y2, pen = 'y')
            else:
                plot.addItem(curve2)
        else:
            plot.removeItem(curve2)

#A widget to hold all of my future widgets
widget_holder = QtGui.QWidget()

#Checkboxes named A1 and A2
cbx1 = QtWidgets.QCheckBox()
cbx1.setText('A1')
cbx1.stateChanged.connect(todo)
b1st = False
curve1 = None

cbx2 = QtWidgets.QCheckBox()
cbx2.setText('A2')
cbx2.stateChanged.connect(todo)
b2st = False
curve2 = None

#Making a pyqtgraph plot widget
plot = pg.PlotWidget()

#Setting the layout
layout = QtGui.QGridLayout()
widget_holder.setLayout(layout)

#Adding the widgets to the layout
layout.addWidget(cbx1, 0,0)
layout.addWidget(cbx2, 0, 1)
layout.addWidget(plot, 1,0, 3,1)

widget_holder.adjustSize()
widget_holder.show()

sys.exit(app.exec_())
"""