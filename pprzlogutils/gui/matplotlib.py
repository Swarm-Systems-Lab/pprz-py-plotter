"""
pprzlogutils - A Python library for parsing and processing Paparazzi UAV log files.

matplotlib provides the graphing GUI for the application based in Qt5.

Author: Pelochus
Date: July 2024
"""

import pprzlogutils.logparser as lp

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#####################################################################
#####################################################################
# Matplotlib section
# Related and useful Links:
# https://matplotlib.org/stable/gallery/index.html
#####################################################################
#####################################################################

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=16, height=9, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.points = False

        super().__init__(fig)
        self.setParent(parent)

    # Plot a single variable
    def plot_var(self, id, message, var):
        v = lp.convert_var_to_numpy(id, message, var)

        if len(v[0]) == 1: # If v not a matrix, x axis is time
            if not self.points:
                self.axes.plot(v, label=message + ' - ' + var)
            else:
                self.axes.plot(v, 'o', markersize=2, label=message + ' - ' + var)
        else: # If var is an array, x axis is the array index
            print("Using scatter plot because selected variable is an array")

            v1 = []
            v2 = []
            for i in range(len(v)):
                v1.append(v[i][0])
                v2.append(v[i][1])
            
            self.axes.scatter(v1, v2, s=10, label=message + ' - ' + var)

    # Plot every variable that is checked
    def plot_checked(self, id, checkboxes):
        for message in checkboxes.keys():
            for var in checkboxes[message]:
                if checkboxes[message][var]:
                    self.plot_var(id, message, var)

    # Draw plot with new checked variables
    def refresh_plot(self, id, checkboxes):
        self.axes.clear()

        self.axes.grid(True)
        self.axes.minorticks_on()
        self.axes.tick_params(which='both', direction='in', top=True, right=True)
        self.axes.grid(True, which='both', linewidth=0.4)
        self.axes.grid(True, which='major', linewidth=1.2)

        self.plot_checked(id, checkboxes)
        self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.draw()

    # Searchbox for messages in dimensional_plot function
    def search_messages(self, text, ordered_keys):
        for message in ordered_keys:
            if text.lower() in message.lower():
                return message