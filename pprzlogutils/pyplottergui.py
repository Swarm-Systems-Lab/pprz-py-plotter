"""
pprzlogutils - A Python library for parsing and processing Paparazzi UAV log files.

pyplottergui provides the GUI for the application based in Qt5.

Author: Pelochus
Date: July 2024
"""

import webbrowser
import pprzlogutils.logparser as lp

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

'''
    Main GUI class, based on PyQt5
'''
class pyplottergui(QMainWindow):
    def __init__(self, log, data):
        super().__init__()

        self.log_path = log
        self.data_path = data

        # Parse log file and create structure
        lp.make_messages_xml(self.log_path.read())
        lp.create_structs(lp.TELEMETRY_OUTPUT_FILENAME)
        lp.create_structs(lp.DATALINK_OUTPUT_FILENAME)

        # Parse data file and fill structure
        lp.parse_datafile(self.data_path)

        # Main window config
        self.setWindowTitle('pprz-py-plotter')
        self.setGeometry(600, 600, 800, 400)
        self.setWindowIcon(QIcon('img/logo.png'))

        # Checkboxes dictionary
        self.checkboxes = {}
        self.current_id = None

        # Menu bar
        self.menubar = self.menuBar()

        # File menu
        fileMenu = self.menubar.addMenu('File')
        
        newWindowAction = QAction('New Window', self)
        newWindowAction.setStatusTip('Open a new window')
        newWindowAction.triggered.connect(self.open_new_window)
        fileMenu.addAction(newWindowAction)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # ID selection menu
        self.id_menu()

        # Messages menu, see function below
        self.messages_menu()

        # Help menu
        helpMenu = self.menubar.addMenu('Help')

        aboutAction = QAction('About (GitHub repo)', self)
        aboutAction.setStatusTip('Show application GitHub repo')
        aboutAction.triggered.connect(self.open_about_url)
        helpMenu.addAction(aboutAction)

        # Show matplotlib canvas in the center of the window
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)
        self.canvas = MplCanvas(self, width=16, height=10, dpi=100)
        layout.addWidget(self.canvas)

        # Add refresh plot button
        refreshButton = QPushButton('Refresh Plot', self)
        refreshButton.setShortcut(QKeySequence(Qt.Key_F5))
        refreshButton.setToolTip('Refresh the plot (F5)')
        refreshButton.clicked.connect(lambda: self.canvas.refresh_plot(self.current_id, self.checkboxes))

        # Add clear all checks button
        clearButton = QPushButton('Clear Checkboxes', self)
        clearButton.setShortcut(QKeySequence(Qt.Key_F4))
        clearButton.setToolTip('Clear all checkboxes (F4)')
        clearButton.clicked.connect(lambda: self.clear_checkboxes())

        # Add to layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(refreshButton)
        buttonLayout.addWidget(clearButton)
        layout.addLayout(buttonLayout)

        self.show()

    def open_new_window(self):
        new_window = pyplottergui(self.log_path, self.data_path)
        new_window.show()

    def open_about_url(self):
        webbrowser.open('https://github.com/Pelochus/pprz-py-plotter')

    '''
        ID select menu
        Choose an UAV ID to plot
        If you want to plot more than one ID, open a new window
    '''
    def id_menu(self):
        idMenu = self.menubar.addMenu('IDs')
        idGroup = QActionGroup(self)

        ids = []
        for id in lp.DATA_DICT.keys():
            ids.append(QAction('ID ' + str(id), self))
            ids[-1].setCheckable(True)
            ids[-1].setChecked(False)
            ids[-1].triggered.connect(lambda: self.handle_id_checkbox(ids[-1], id))
            idGroup.addAction(ids[-1])
            idMenu.addAction(ids[-1])
    
    '''
        Messages select menu. 
        Select a message and its variables to plot
    '''
    def messages_menu(self):
        editMenu = self.menubar.addMenu('Messages')

        # Better added in groups, so the menu is not too long
        msg_a_c = editMenu.addMenu('A-C')
        msg_a_c.setStatusTip('Messages A to C included')

        msg_d_f = editMenu.addMenu('D-F')
        msg_d_f.setStatusTip('Messages D to F included')

        msg_g_i = editMenu.addMenu('G-I')
        msg_g_i.setStatusTip('Messages G to I included')

        msg_j_l = editMenu.addMenu('J-L')
        msg_j_l.setStatusTip('Messages J to L included')

        msg_m_o = editMenu.addMenu('M-O')
        msg_m_o.setStatusTip('Messages M to O included')

        msg_p_r = editMenu.addMenu('P-R')
        msg_p_r.setStatusTip('Messages P to R included')

        msg_s_u = editMenu.addMenu('S-U')
        msg_s_u.setStatusTip('Messages S to U included')

        msg_v_z = editMenu.addMenu('V-Z')
        msg_v_z.setStatusTip('Messages V to Z included')

        msg_submenus = []
        ordered_keys = sorted(lp.MESSAGES_TYPES.keys(), key=str.lower) # Alphabetical order
        for message in ordered_keys:
            # Create inner dict
            self.checkboxes[message] = {}

            # Friendly reminder, -1 is last element
            if message[0] in 'ABC':
                msg_submenus.append(msg_a_c.addMenu(message))
            elif message[0] in 'DEF':
                msg_submenus.append(msg_d_f.addMenu(message))
            elif message[0] in 'GHI':
                msg_submenus.append(msg_g_i.addMenu(message))
            elif message[0] in 'JKL':
                msg_submenus.append(msg_j_l.addMenu(message))
            elif message[0] in 'MNO':
                msg_submenus.append(msg_m_o.addMenu(message))
            elif message[0] in 'PQR':
                msg_submenus.append(msg_p_r.addMenu(message))
            elif message[0] in 'STU':
                msg_submenus.append(msg_s_u.addMenu(message))
            else:
                msg_submenus.append(msg_v_z.addMenu(message))
 
            # Add the variables to the submenu as checkboxes
            for var in lp.MESSAGES_TYPES[message]._fields:
                action = QAction(var, self)
                action.setCheckable(True)
                action.setChecked(False)
                
                action.triggered.connect(lambda checked, m=message, v=var: self.handle_checkbox(checked, m, v))
                msg_submenus[-1].addAction(action)

                # Initialize all to false
                self.checkboxes[message][var] = False

    '''
        Lambdas for handling checkboxes
    '''
    def handle_id_checkbox(self, idcheck, id):
        if idcheck.isChecked():
            self.current_id = id
            print("Current ID selected:", self.current_id)
        else:
            pass

    def handle_checkbox(self, checked, message, var):
        if checked:
            self.checkboxes[message][var] = True
        else:
            self.checkboxes[message][var] = False
            pass

    # TODO: Do properly, GUIs' checkboxes are still checked, only self.checkboxes is cleared
    def clear_checkboxes(self):
        for message in self.checkboxes.keys():
            for var in self.checkboxes[message]:
                self.checkboxes[message][var] = False

#####################################################################
#####################################################################
# Matplotlib section
# Related and useful Links:
# https://matplotlib.org/stable/gallery/index.html
#####################################################################
#####################################################################

'''
    Matplotlib canvas class

    This displays a matplotlib graph on the center of the window
'''
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=16, height=9, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        super().__init__(fig)
        self.setParent(parent)
        
        self.plot_example()

    # Default plot, as an example
    def plot_example(self):
        x = [0, 1, 2, 3, 4]
        y = [0, 1, 4, 9, 16]
        self.axes.plot(x, y, label='Default plot')
        self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.draw()

    # Plot a single variable
    def plot_var(self, id, message, var):
        self.axes.plot(lp.convert_var_to_numpy(id, message, var), label=message + ' - ' + var)

    # Plot every variable that is checked
    def plot_checked(self, id, checkboxes):
        for message in checkboxes.keys():
            for var in checkboxes[message]:
                if checkboxes[message][var]:
                    self.plot_var(id, message, var)

    # Draw plot with new checked variables
    def refresh_plot(self, id, checkboxes):
        self.axes.clear()
        self.plot_checked(id, checkboxes)
        self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.draw()