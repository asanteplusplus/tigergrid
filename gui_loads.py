# This Class Sets Up the Graphical User Interface of the Loads Page 
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage 
import smart.globals as globals
                     
class loads_ui(QWidget):  
    def setup(self, window):   
        
        self.main_window = window
        labelFont=QFont("Futura", 20)          
        
        title1 = QLabel('Select Climate Zone')
        title1.setFont(labelFont)
        title1.setStyleSheet('color: orange')

        koppen = QLabel('Koppen-Geiger Classification')
        koppen.setFont(labelFont)
        koppen.setStyleSheet('color: orange')

        space = QLabel('                  ')
        space.setFont(labelFont)
        
        title2 = QLabel('Select Load Type')
        title2.setStyleSheet('color: orange')
        title2.setFont(labelFont)
  
        pixmap = QPixmap('rsz_kop.png')
        self.image = QLabel()
        self.image.setPixmap(pixmap)
        self.image.setGeometry(60, 40, 100, 200)

        # Code for the Climate zones
        Af = QPushButton('Af', self)
        Af.setCheckable(True)
        Af.clicked[bool].connect(self.setZone)

        Am = QPushButton('Am', self)
        Am.setCheckable(True)
        Am.setFixedWidth(200)
        Am.clicked[bool].connect(self.setZone)

        Aw = QPushButton('Aw', self)
        Aw.setCheckable(True)
        Aw.clicked[bool].connect(self.setZone)

        As = QPushButton('As', self)
        As.setCheckable(True)
        As.setFixedWidth(200)
        As.clicked[bool].connect(self.setZone)

        BWh = QPushButton('BWh', self)
        BWh.setCheckable(True)
        BWh.clicked[bool].connect(self.setZone)

        BWk = QPushButton('BWk', self)
        BWk.setCheckable(True)
        BWk.setFixedWidth(200)
        BWk.clicked[bool].connect(self.setZone)

        BSh = QPushButton('BSh', self)
        BSh.setCheckable(True)
        BSh.clicked[bool].connect(self.setZone)

        BSk = QPushButton('BSk', self)
        BSk.setCheckable(True)
        BSk.setFixedWidth(200)
        BSk.clicked[bool].connect(self.setZone)

        Csa = QPushButton('Csa', self)
        Csa.setCheckable(True)
        Csa.clicked[bool].connect(self.setZone)

        Csb = QPushButton('Csb', self)
        Csb.setCheckable(True)
        Csb.setFixedWidth(200)
        Csb.clicked[bool].connect(self.setZone)

        Csc = QPushButton('Csc', self)
        Csc.setCheckable(True)
        Csc.clicked[bool].connect(self.setZone)

        Cwa = QPushButton('Cwa', self)
        Cwa.setCheckable(True)
        Cwa.setFixedWidth(200)
        Cwa.clicked[bool].connect(self.setZone)

        Cwb = QPushButton('Cwb', self)
        Cwb.setCheckable(True)
        Cwb.clicked[bool].connect(self.setZone)

        Cwc = QPushButton('Cwc', self)
        Cwc.setCheckable(True)
        Cwc.setFixedWidth(200)
        Cwc.clicked[bool].connect(self.setZone)

        Cfa = QPushButton('Cfa', self)
        Cfa.setCheckable(True)
        Cfa.clicked[bool].connect(self.setZone)

        Cfb = QPushButton('Cfb', self)
        Cfb.setCheckable(True)
        Cfb.setFixedWidth(200)
        Cfb.clicked[bool].connect(self.setZone)

        Cfc = QPushButton('Cfc', self)
        Cfc.setCheckable(True)
        Cfc.clicked[bool].connect(self.setZone)

        Dsa = QPushButton('Dsa', self)
        Dsa.setCheckable(True)
        Dsa.setFixedWidth(200)
        Dsa.clicked[bool].connect(self.setZone)

        Dsb = QPushButton('Dsb', self)
        Dsb.setCheckable(True)
        Dsb.clicked[bool].connect(self.setZone)

        Dsc = QPushButton('Dsc', self)
        Dsc.setCheckable(True)
        Dsc.setFixedWidth(200)
        Dsc.clicked[bool].connect(self.setZone)

        Dsd = QPushButton('Dsd', self)
        Dsd.setCheckable(True)
        Dsd.clicked[bool].connect(self.setZone)

        Dwa = QPushButton('Dwa', self)
        Dwa.setCheckable(True)
        Dwa.setFixedWidth(200)
        Dwa.clicked[bool].connect(self.setZone)

        Dwb = QPushButton('Dwb', self)
        Dwb.setCheckable(True)
        Dwb.clicked[bool].connect(self.setZone)

        Dwc = QPushButton('Dwc', self)
        Dwc.setCheckable(True)
        Dwc.setFixedWidth(200)
        Dwc.clicked[bool].connect(self.setZone)

        Dwd = QPushButton('Dwd', self)
        Dwd.setCheckable(True)
        Dwd.clicked[bool].connect(self.setZone)

        Dfa = QPushButton('Dfa', self)
        Dfa.setCheckable(True)
        Dfa.setFixedWidth(200)
        Dfa.clicked[bool].connect(self.setZone)

        Dfb = QPushButton('Dfb', self)
        Dfb.setCheckable(True)
        Dfb.clicked[bool].connect(self.setZone)

        Dfc = QPushButton('Dfc', self)
        Dfc.setCheckable(True)
        Dfc.setFixedWidth(200)
        Dfc.clicked[bool].connect(self.setZone)

        Dfd = QPushButton('Dfd', self)
        Dfd.setCheckable(True)
        Dfd.clicked[bool].connect(self.setZone)

        ET = QPushButton('ET', self)
        ET.setCheckable(True)
        ET.setFixedWidth(200)
        ET.clicked[bool].connect(self.setZone)

        EF = QPushButton('EF', self)
        EF.setCheckable(True)
        EF.setFixedWidth(400)
        EF.clicked[bool].connect(self.setZone)

        update_button = QPushButton("Download Load Data from OpenEI Database", clicked=self.update_data)
        input_load_lbl = QLabel('Input the Average Load for System')
        input_load_lbl.setStyleSheet('color: beige')
        input_load_lbl.setFont(QFont("Segoe UI", 15) )
        input_load_unit = QLabel('KWh/d')
        input_load_unit.setStyleSheet('color: beige')
        self.input_load = QLineEdit()
        self.input_load.setFixedWidth(100)

        altload_title = QLabel('Alternatively, Use the Average Load for your System, if Known')
        altload_title.setStyleSheet('color: orange')
        altload_title.setFont(labelFont)
        altload_btn = QPushButton("Click to Use this Load Instead",clicked=self.update_altload)

        self.load_types = QComboBox()
        self.load_types.addItems(["Full Service Restaurant model: 5,500 square feet, 1 floor",
                                  "Hospital model: 241,351 square feet, 5 floors",
                                  "Large Hotel model: 122,120 square feet, 6 floors",
                                  "Large Office model: 498,588 square feet, 12 floor",
                                  "Medium Office model: 52,628 square feet, 3 floor",
                                  "Midrise Appartment model: 33,740 square feet, 4 floors",
                                  "Out Patient Clinic model: 40,946 square feet, 3 floors",
                                  "Primary School model: 73,960 square feet, 1 floor",
                                  "Quick Service Restaurant model: 2,500 square feet, 1 floor",
                                  "Secondary School model: 210,887 square feet, 2 floors",
                                  "Small Hotel model: 43,200 square feet, 4 floors",
                                  "Small Office model: 5,500 square feet, 1 floor",
                                  "Stand-alone Retail model: 24,962 square feet, 1 floor",
                                  "Strip Mall model: 22,500 square feet, 1 floor",
                                  "Supermarket model: 45,000 square feet, 1 floor",
                                  "Warehouse model: 52,045 square feet, 1 floor"])

        layout = QGridLayout()
        layout.addWidget(title1, 0, 0)
        layout.addWidget(Af, 1, 0)
        layout.addWidget(Am, 1, 1)
        layout.addWidget(Aw, 2, 0)
        layout.addWidget(As, 2, 1)
        layout.addWidget(BWh, 3, 0)
        layout.addWidget(BWk, 3, 1)
        layout.addWidget(BSh, 4, 0)
        layout.addWidget(BSk, 4, 1)
        layout.addWidget(Csa, 5, 0)
        layout.addWidget(Csb, 5, 1)
        layout.addWidget(Csc, 6, 0)
        layout.addWidget(Cwa, 6, 1)
        layout.addWidget(Cwb, 7, 0)
        layout.addWidget(Cwc, 7, 1)
        layout.addWidget(Cfa, 8, 0)
        layout.addWidget(Cfb, 8, 1)
        layout.addWidget(Cfc, 9, 0)
        layout.addWidget(Dsa, 9, 1)
        layout.addWidget(Dsb, 10, 0)
        layout.addWidget(Dsc, 10, 1)
        layout.addWidget(Dsd, 11, 0)
        layout.addWidget(Dwa, 11, 1)
        layout.addWidget(Dwb, 12, 0)
        layout.addWidget(Dwc, 12, 1)
        layout.addWidget(Dwd, 13, 0)
        layout.addWidget(Dfa, 13, 1)
        layout.addWidget(Dfb, 14, 0)
        layout.addWidget(Dfc, 14, 1)
        layout.addWidget(Dfd, 15, 0)
        layout.addWidget(ET, 15, 1)
        layout.addWidget(EF, 16, 0, 1, 4)
        layout.addWidget(title2, 12, 6, 1, 3)
        layout.addWidget(self.load_types, 13, 6, 1, 2)
        layout.addWidget(update_button, 13, 10, 1, 3)
        layout.addWidget(altload_title, 14, 6, 1, 6)
        layout.addWidget(input_load_lbl, 15, 6)
        layout.addWidget(self.input_load, 15, 7)
        layout.addWidget(input_load_unit, 15, 8)
        layout.addWidget(altload_btn, 15, 10, 1, 3)
        layout.addWidget(koppen, 0, 6, 1, 3)
        layout.addWidget(space, 0, 5)
        layout.addWidget(self.image, 1, 6, 10, 200)
        
        self.setLayout(layout)  
        self.load_index = str(self.load_types.currentIndex())
        self.zone_index = globals.zone
        globals.load_kwhd = globals.zoneLoadDict[self.zone_index][self.load_index]

    # Method Updates the Global Variables
    def update_data(self):
        self.load_index = str(self.load_types.currentIndex())
        self.zone_index = globals.zone
        if globals.load_kwhd == str(self.input_load.text()):
            pass
        else:
            globals.load_kwhd = globals.zoneLoadDict[self.zone_index][self.load_index]
        self.main_window.show_status_message('Load data succcessfully downloaded from OpenEI database')

    # Method Updates the Global Load Variable with the User Input     
    def update_altload(self):
        globals.load_kwhd = str(self.input_load.text())
        print(globals.load_kwhd)
        self.main_window.show_status_message('Success! System Load Updated')

    # Method Updates the Global Zone Variable with the Selected Zone    
    def setZone(self, pressed):
        source = self.sender()
        if pressed:
            val = 255
        else: val = 0
        globals.zone = source.text()
           