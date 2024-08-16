"""
pprzlogutils - A Python library for parsing and processing Paparazzi UAV log files.

pyplottergui provides the GUI for the application based in Qt5.

Author: Pelochus
Date: July 2024
"""

import webbrowser
import pprzlogutils.logparser as lp
import pprzlogutils.gui.matplotlib as mpl

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QCheckBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

#####################################################################
#####################################################################
# Main GUI class, using PyQt5
#####################################################################
#####################################################################

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
        
        # TODO: Fix open_new_window, then uncomment this
        '''
        newWindowAction = QAction('New Window', self)
        newWindowAction.setStatusTip('Open a new window')
        newWindowAction.triggered.connect(self.open_new_window)
        fileMenu.addAction(newWindowAction)
        '''

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
        self.canvas = mpl.MplCanvas(self, width=16, height=10, dpi=100)
        layout.addWidget(self.canvas)

        # Add clear all checks button
        clearButton = QPushButton('Clear Checkboxes', self)
        clearButton.setShortcut(QKeySequence(Qt.Key_F4))
        clearButton.setToolTip('Clear all checkboxes (F4)')
        clearButton.clicked.connect(lambda: self.clear_checkboxes())

        # Add refresh plot button
        refreshButton = QPushButton('Refresh Plot', self)
        refreshButton.setShortcut(QKeySequence(Qt.Key_F5))
        refreshButton.setToolTip('Refresh the plot (F5)')
        refreshButton.clicked.connect(lambda: self.canvas.refresh_plot(self.current_id, self.checkboxes))

        # Add clear all checks button
        pointsButton = QPushButton('Points/Lines', self)
        pointsButton.setShortcut(QKeySequence(Qt.Key_F6))
        pointsButton.setToolTip('Select between points or lines plots (F6)')
        pointsButton.clicked.connect(lambda: self.points_lines())

        # Add to layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(clearButton)
        buttonLayout.addWidget(refreshButton)
        buttonLayout.addWidget(pointsButton)
        layout.addLayout(buttonLayout)

        self.show()

    # TODO: Broken, for now launch one new window manually
    '''
    def open_new_window(self):
        new_window = pyplottergui(self.log_path, self.data_path)
        new_window.show()
    '''

    def open_about_url(self):
        webbrowser.open('https://github.com/Swarm-Systems-Lab/pprz-py-plotter')

    '''
        ID select menu
        Choose an UAV ID to plot
        If you want to plot more than one ID, open a new window
    '''
    def id_menu(self):
        idMenu = self.menubar.addMenu('IDs')
        idGroup = QActionGroup(self)

        ids = []
        num_id = []
        found_ids = sorted(lp.DATA_DICT.keys())

        for id in found_ids: 
            num_id.append(id) # Save number for later
            ids.append(QAction('ID ' + str(id), self))
            
        for i in range(0, len(ids)):
            ids[i].setCheckable(True)
            ids[i].setChecked(False)
            ids[i].triggered.connect(lambda checked, ni=num_id[i]: self.handle_id_checkbox(checked, ni))
                                     
            idGroup.addAction(ids[i])
            idMenu.addAction(ids[i])
    
    '''
        Messages select menu. 
        Select a message and its variables to plot
    '''
    def messages_menu(self):
        msgMenu = self.menubar.addMenu('Messages')

        # Better added in groups, so the menu is not too long
        # Recommended to be edited with Copilot!
        msg_a_b = msgMenu.addMenu('A-B')
        msg_a_b.setStatusTip('Messages A to B included')

        msg_c_d = msgMenu.addMenu('C-D')
        msg_c_d.setStatusTip('Messages C to D included')

        msg_e_f = msgMenu.addMenu('E-F')
        msg_e_f.setStatusTip('Messages E to F included')

        msg_g_h = msgMenu.addMenu('G-H')
        msg_g_h.setStatusTip('Messages G to H included')

        msg_i_j = msgMenu.addMenu('I-J')
        msg_i_j.setStatusTip('Messages I to J included')

        msg_k_l = msgMenu.addMenu('K-L')
        msg_k_l.setStatusTip('Messages K to L included')

        msg_m_n = msgMenu.addMenu('M-N')
        msg_m_n.setStatusTip('Messages M to N included')

        msg_o_p = msgMenu.addMenu('O-P')
        msg_o_p.setStatusTip('Messages O to P included')

        msg_q_r = msgMenu.addMenu('Q-R')
        msg_q_r.setStatusTip('Messages Q to R included')

        msg_s_t = msgMenu.addMenu('S-T')
        msg_s_t.setStatusTip('Messages S to T included')

        msg_u_v = msgMenu.addMenu('U-V')
        msg_u_v.setStatusTip('Messages U to V included')

        msg_w_x = msgMenu.addMenu('W-X')
        msg_w_x.setStatusTip('Messages W to X included')

        msg_y_z = msgMenu.addMenu('Y-Z')
        msg_y_z.setStatusTip('Messages Y to Z included')

        msg_submenus = []
        ordered_keys = sorted(lp.MESSAGES_TYPES.keys(), key=str.lower) # Alphabetical order
        for message in ordered_keys:
            # Create inner dict
            self.checkboxes[message] = {}

            if message[0] in 'AB':
                msg_submenus.append(msg_a_b.addMenu(message))
            elif message[0] in 'CD':
                msg_submenus.append(msg_c_d.addMenu(message))
            elif message[0] in 'EF':
                msg_submenus.append(msg_e_f.addMenu(message))
            elif message[0] in 'GH':
                msg_submenus.append(msg_g_h.addMenu(message))
            elif message[0] in 'IJ':
                msg_submenus.append(msg_i_j.addMenu(message))
            elif message[0] in 'KL':
                msg_submenus.append(msg_k_l.addMenu(message))
            elif message[0] in 'MN':
                msg_submenus.append(msg_m_n.addMenu(message))
            elif message[0] in 'OP':
                msg_submenus.append(msg_o_p.addMenu(message))
            elif message[0] in 'QR':
                msg_submenus.append(msg_q_r.addMenu(message))
            elif message[0] in 'ST':
                msg_submenus.append(msg_s_t.addMenu(message))
            elif message[0] in 'UV':
                msg_submenus.append(msg_u_v.addMenu(message))
            elif message[0] in 'WX':
                msg_submenus.append(msg_w_x.addMenu(message))
            else:
                msg_submenus.append(msg_y_z.addMenu(message))
 
            # Add the variables to the submenu as checkboxes
            for var in lp.MESSAGES_TYPES[message]._fields:
                checkBox = QCheckBox(var, msg_submenus[-1])
                checkableAction = QWidgetAction(msg_submenus[-1])
                checkableAction.setDefaultWidget(checkBox)
                checkBox.stateChanged.connect(lambda state, m=message, v=var: self.handle_checkbox(state, m, v))
                
                msg_submenus[-1].addAction(checkableAction)
                self.checkboxes[message][var] = False # Initialize all to false


    #####################################################################
    #####################################################################
    # Lambdas
    #####################################################################
    #####################################################################


    # Handle ID checkbox selection
    def handle_id_checkbox(self, idchecked, id):
        if idchecked:
            self.current_id = id            
            for msg_name in lp.DATA_DICT[self.current_id].keys():
                for submenu in self.menubar.actions():
                    if submenu.text() == 'Messages':
                        for action in submenu.menu().actions(): # A-B, C-D... submenus
                            for subaction in action.menu().actions(): # Messages names submenu
                                if isinstance(subaction, QAction):
                                    if subaction.text() == msg_name:
                                        font = subaction.font()
                                        font.setUnderline(True) # Underline messages available for that ID
                                        subaction.setFont(font)
            self.update()
        else:
            pass

    # Handle checkboxes (message/variable menu)
    def handle_checkbox(self, checked, message, var):
        if checked:
            self.checkboxes[message][var] = True
        else:
            self.checkboxes[message][var] = False
    
    # Clear all checkboxes, interface and data
    def clear_checkboxes(self):
        # Clear boolean array
        for message in self.checkboxes.keys():
            for var in self.checkboxes[message]:
                self.checkboxes[message][var] = False

        # Clear checkboxes in the Messages menu
        for action in self.menubar.actions():
            if action.text() == 'Messages':
                for submenu in action.menu().actions(): # A-B, C-D... submenus
                    for subaction in submenu.menu().actions(): # Messages names submenu
                        for checkbox in subaction.menu().actions(): # Actual checkbox
                            if isinstance(checkbox, QWidgetAction):
                                checkbox.defaultWidget().setChecked(False)
                                
        self.update()
        self.canvas.refresh_plot(self.current_id, self.checkboxes)

    # Handle showing plot or line based plots
    def points_lines(self):
        if self.canvas.points:
            self.canvas.points = False
        else:
            self.canvas.points = True

        self.canvas.refresh_plot(self.current_id, self.checkboxes)