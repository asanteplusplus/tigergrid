#This Class Sets Up the Graphical User Interface of the Solar PV Page
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuickWidgets, QtPositioning
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import smart.globals as globals
                    
class solar_ui(QWidget): 
    def setup(self, window):
        
        self.main_window = window
        labelFont=QFont("Futura", 20)         
        
        title1 = QLabel('Site Location')
        title1.setStyleSheet('color: orange')
        title1.setFont(labelFont)
        
        label1 = QLabel('Latitude:')
        label1.setStyleSheet('color: beige')
        label1.setFixedWidth(100)
        
        self.edit_lat = QLineEdit()
        self.edit_lat.setFixedWidth(200)

        labelz = QLabel('Site Address:')
        labelz.setStyleSheet('color: beige')
        labelz.setFixedWidth(100)
        
        self.edit_addr = QLineEdit()
        self.edit_addr.setFixedWidth(200)
        
        label2 = QLabel('Longitude:')
        label2.setStyleSheet('color: beige')
        label2.setFixedWidth(100)
        
        self.edit_lon = QLineEdit()
        self.edit_lon.setFixedWidth(200)
        
        title2 = QLabel('Solar resource data')
        title2.setStyleSheet('color: orange')
        title2.setFont(labelFont)
        
        update_button = QPushButton("Update")
        update_button.setFixedWidth(120)
  
        vline = QFrame()
        vline.setFrameStyle(QFrame.VLine | QFrame.Sunken)
        
        title3 = QLabel('Solar PV system')
        title3.setStyleSheet('color: orange')
        title3.setFont(labelFont)
        
        label4a = QLabel('PV Module Efficiency:')
        label4a.setStyleSheet('color: beige')
        label4b = QLabel('0 < n< 1')
        label4b.setStyleSheet('color: beige')
        
        self.PV_Efficiency = QLineEdit()
        self.PV_Efficiency.setFixedWidth(100)

        pvcap_label = QLabel('PV Capacity:')
        pvcap_label.setStyleSheet('color: beige')
        pvcap_unit = QLabel('kW')
        pvcap_unit.setStyleSheet('color: beige')
        
        self.pvcap = QLineEdit()
        self.pvcap.setFixedWidth(100)

        pvbrand_label = QLabel('Solar Panel Brand:')
        pvbrand_label.setStyleSheet('color: beige')
        
        self.pvbrand = QLineEdit()
        self.pvbrand.setFixedWidth(300)
        
        label6a = QLabel('PV Temperature Derating:')
        label6a.setStyleSheet('color: beige')
        label6b = QLabel('percent per degree celsius')
        label6b.setStyleSheet('color: beige')
        
        self.Temp_Derating = QLineEdit()
        self.Temp_Derating.setFixedWidth(100)
        
        label7a = QLabel('Wiring Efficiency:')
        label7a.setStyleSheet('color: beige')
        label7b = QLabel('0 < n < 1')
        label7b.setStyleSheet('color: beige')
        
        self.wiring_eff = QLineEdit()
        self.wiring_eff.setFixedWidth(100)
        
       
        label8a = QLabel('Area of PV Module:')
        label8a.setStyleSheet('color: beige')
        label8b = QLabel('sq. metres')
        label8b.setStyleSheet('color: beige')
        
        self.PV_Area = QLineEdit()
        self.PV_Area.setFixedWidth(100)
        
        horispace = QLabel('               ')

        label10a = QLabel('Inverter efficiency:')
        label10a.setStyleSheet('color: beige')
        label10b = QLabel('0 < n < 1')
        label10b.setStyleSheet('color: beige')
        
        self.Inverter_eff = QLineEdit()
        self.Inverter_eff.setFixedWidth(100)
        
        label11a = QLabel('Tilt angle:')
        label11a.setStyleSheet('color: beige')
        label11b = QLabel('degrees')
        label11b.setStyleSheet('color: beige')
        
        self.edit_tilt = QLineEdit()
        self.edit_tilt.setFixedWidth(100)

        pixmap = QPixmap('spanel.png')
        self.image = QLabel()
        self.image.setPixmap(pixmap)
        self.image.setGeometry(1, 14, 15, 100)
        
        self.pv_models =     {
                'Capacity': {
                        'CanadianSolar All-Black CS6K-290MS': '0.29', 
                        'CanadianSolar Dymond CS6K-285M-FG': '0.285', 
                        'CanadianSolar MaxPower CS6U-330P': '0.33', 
                        'CanadianSolar MaxPower CS6U-340M': '0.34', 
                        'CanadianSolar MaxPower CS6X-325P': '0.325', 
                        'CanadianSolar Quintech CS6K-285M': '0.285', 
                        'CanadianSolar SuperPower CS6K-295MS': '0.295'
                        },
                'Derating': {
                        'CanadianSolar All-Black CS6K-290MS': '88', 
                        'CanadianSolar Dymond CS6K-285M-FG': '88', 
                        'CanadianSolar MaxPower CS6U-330P': '88', 
                        'CanadianSolar MaxPower CS6U-340M': '88', 
                        'CanadianSolar MaxPower CS6X-325P': '88', 
                        'CanadianSolar Quintech CS6K-285M': '88', 
                        'CanadianSolar SuperPower CS6K-295MS': '88'
                        },
                'Efficiencies': {
                        'CanadianSolar All-Black CS6K-290MS': '17.7', 
                        'CanadianSolar Dymond CS6K-285M-FG': '17.3', 
                        'CanadianSolar MaxPower CS6U-330P': '17', 
                        'CanadianSolar MaxPower CS6U-340M': '17.5', 
                        'CanadianSolar MaxPower CS6X-325P': '16.9', 
                        'CanadianSolar Quintech CS6K-285M': '17.4', 
                        'CanadianSolar SuperPower CS6K-295MS': '18' 
                        },
                'Coefficient': {
                        'CanadianSolar All-Black CS6K-290MS': '-0.39', 
                        'CanadianSolar Dymond CS6K-285M-FG': '-0.41', 
                        'CanadianSolar MaxPower CS6U-330P': '-0.41', 
                        'CanadianSolar MaxPower CS6U-340M': '-0.41', 
                        'CanadianSolar MaxPower CS6X-325P': '-0.41', 
                        'CanadianSolar Quintech CS6K-285M': '-0.41', 
                        'CanadianSolar SuperPower CS6K-295MS': '-0.39'
                        },
                'Brands': {
                        'CanadianSolar All-Black CS6K-290MS': 'Canadian Solar', 
                        'CanadianSolar Dymond CS6K-285M-FG': 'Canadian Solar', 
                        'CanadianSolar MaxPower CS6U-330P': 'Canadian Solar', 
                        'CanadianSolar MaxPower CS6U-340M': 'Canadian Solar', 
                        'CanadianSolar MaxPower CS6X-325P': 'Canadian Solar', 
                        'CanadianSolar Quintech CS6K-285M': 'Canadian Solar', 
                        'CanadianSolar SuperPower CS6K-295MS': 'Canadian Solar'
                        }
                }

        self.inverter_data = {
                'Efficiencies': {
                        'CyboEnergy Grid-Interactive C1-Mini-1000A': '0.96', 
                        'CyboEnergy Off-Grid C1-Mini-1000N': '0.96', 
                        'Eaton Power Xpert 1000kW': '0.98', 
                        'Eaton Power Xpert 1500kW': '0.98', 
                        'Eaton Power Xpert 2000kW': '0.98', 
                        'Eaton Power Xpert 2250kW': '0.98', 
                        'Fronius Symo 20.0-3-M': '0.98', 
                        'Fronius Symo 8.2-3-M': '0.98', 
                        'Fronius Galvo 2.5-1': '0.95', 
                        'Fronius Primo 8.2-1': '0.97', 
                        'Fronius Symo 4.5-3-S': '0.97', 
                        'Leonics MTP-4117H 300kW': '0.96',
                        'Leonics MTP-413F 25kW': '0.96', 
                        'Leonics S-219Cp 5kW': '0.96', 
                        'Leonics STP-219Cp 15kW': '0.96', 
                        'Leonics GTP-507 125kW': '0.96', 
                        'Magnum MS4448PAE': '0.94'
                        }
                     }


        pv_label = QLabel('Solar PV Model')
        pv_label.setStyleSheet('color: orange')
        pv_label.setFont(labelFont)
        self.pv_config = QComboBox()
        self.pv_config.setStyle( QStyleFactory.create( "Polyester" ) )
        self.pv_config.addItems(['CanadianSolar All-Black CS6K-290MS', 'CanadianSolar Dymond CS6K-285M-FG', 'CanadianSolar MaxPower CS6U-330P', 'CanadianSolar MaxPower CS6U-340M', 
                        'CanadianSolar MaxPower CS6X-325P', 'CanadianSolar Quintech CS6K-285M', 'CanadianSolar SuperPower CS6K-295MS'])
        self.pv_config.currentIndexChanged.connect(self.update_brand)

        inv_label = QLabel('Inverter Model')
        inv_label.setStyleSheet('color: orange')
        inv_label.setFont(labelFont)
        self.inv_config = QComboBox()
        self.inv_config.setStyle( QStyleFactory.create( "Polyester" ) )
        self.inv_config.addItems(['CyboEnergy Grid-Interactive C1-Mini-1000A', 'CyboEnergy Off-Grid C1-Mini-1000N', 'Eaton Power Xpert 1000kW', 
                        'Eaton Power Xpert 1500kW', 'Eaton Power Xpert 2000kW', 'Eaton Power Xpert 2250kW', 'Fronius Symo 20.0-3-M', 
                        'Fronius Symo 8.2-3-M', 'Fronius Galvo 2.5-1', 'Fronius Primo 8.2-1', 'Fronius Symo 4.5-3-S', 
                        'Leonics MTP-4117H 300kW','Leonics MTP-413F 25kW', 'Leonics S-219Cp 5kW', 
                        'Leonics STP-219Cp 15kW', 'Leonics GTP-507 125kW', 'Magnum MS4448PAE'])
        self.inv_config.currentIndexChanged.connect(self.update_inverter)

        layout = QGridLayout()
        layout.addWidget(title1, 0, 0)
        layout.addWidget(label1, 2, 0)
        layout.addWidget(self.edit_lat, 2, 1)
        layout.addWidget(label2, 3, 0)
        layout.addWidget(self.edit_lon, 3, 1)
        layout.addWidget(labelz, 1, 0)
        layout.addWidget(self.edit_addr, 1, 1)
        layout.addWidget(update_button, 0, 2)
        layout.addWidget(pv_label, 5, 0)
        layout.addWidget(self.pv_config, 6, 0, 1, 2)
        layout.addWidget(inv_label, 7, 0)
        layout.addWidget(self.inv_config, 8, 0, 1, 2)
        layout.addWidget(title3, 0, 5)
        layout.addWidget(label4a, 2, 5)
        layout.addWidget(self.PV_Efficiency, 2, 6)
        layout.addWidget(label4b, 2, 7)
        layout.addWidget(pvcap_label, 3, 5)
        layout.addWidget(self.pvcap, 3, 6)
        layout.addWidget(pvcap_unit, 3, 7)
        layout.addWidget(pvbrand_label, 1, 5)
        layout.addWidget(self.pvbrand, 1, 6, 1, 3)
        layout.addWidget(label6a, 4, 5)
        layout.addWidget(self.Temp_Derating, 4, 6)
        layout.addWidget(label6b, 4, 7)
        layout.addWidget(label7a, 5, 5)
        layout.addWidget(self.wiring_eff, 5, 6)
        layout.addWidget(label7b, 5, 7)
        layout.addWidget(label8a, 6, 5)
        layout.addWidget(self.PV_Area, 6, 6)
        layout.addWidget(label8b, 6, 7)
        layout.addWidget(label10a, 7, 5)
        layout.addWidget(self.Inverter_eff, 7, 6)
        layout.addWidget(label10b, 7, 7)
        layout.addWidget(label11a, 8, 5)
        layout.addWidget(self.edit_tilt, 8, 6)
        layout.addWidget(label11b, 8, 7)
        layout.addWidget(horispace, 9, 5)
        layout.addWidget(horispace, 10, 5)
        layout.addWidget(self.image, 11, 11, 5, 15)
        self.setLayout(layout)
        
        self.refresh_data()
        update_button.clicked.connect(self.refresh_data)

    # Method Updates the Global Variables
    def update_data(self):
        globals.latitude = float(self.edit_lat.text())
        globals.longitude = float(self.edit_lon.text())
        globals.address = str(self.edit_addr.text())
        globals.pv_data['PV_eff'] = float(self.PV_Efficiency.text())
        globals.pv_data['P_coeff'] = float(self.Temp_Derating.text())
        globals.pv_data['wire_eff'] = float(self.wiring_eff.text())
        globals.pv_data['area'] = float(self.PV_Area.text())
        globals.pv_data['eff_inv'] = float(self.Inverter_eff.text())
        globals.pv_data['tilt'] = float(self.edit_tilt.text())
        globals.pv_data['pvcap'] = float(self.pvcap.text())
        globals.pv_data['pvbrand'] = str(self.pvbrand.text())

    # Method Updates the Global Solar Variables with the User Input     
    def update_brand(self):
        if self.pv_config.currentIndex() == 0:
            globals.pv_data['pvbrand'] = 'CanadianSolar All-Black CS6K-290MS'
            self.pvbrand.setText(str(globals.pv_data['pvbrand']))
            self.pvcap.setText(str(self.pv_models['Capacity'][self.pvbrand.text()]))
            self.PV_Efficiency.setText(str(self.pv_models['Efficiencies'][self.pvbrand.text()]))
            self.Temp_Derating.setText(str(self.pv_models['Coefficient'][self.pvbrand.text()]))

        elif self.pv_config.currentIndex() == 1:
            globals.pv_data['pvbrand'] = 'CanadianSolar Dymond CS6K-285M-FG'
            self.pvbrand.setText(str(globals.pv_data['pvbrand']))
            self.pvcap.setText(str(self.pv_models['Capacity'][self.pvbrand.text()]))
            self.PV_Efficiency.setText(str(self.pv_models['Efficiencies'][self.pvbrand.text()]))
            self.Temp_Derating.setText(str(self.pv_models['Coefficient'][self.pvbrand.text()]))
        elif self.pv_config.currentIndex() == 2:
            globals.pv_data['pvbrand'] = 'CanadianSolar MaxPower CS6U-330P'
            self.pvbrand.setText(str(globals.pv_data['pvbrand']))
            self.pvcap.setText(str(self.pv_models['Capacity'][self.pvbrand.text()]))
            self.PV_Efficiency.setText(str(self.pv_models['Efficiencies'][self.pvbrand.text()]))
            self.Temp_Derating.setText(str(self.pv_models['Coefficient'][self.pvbrand.text()]))
        elif self.pv_config.currentIndex() == 3:
            globals.pv_data['pvbrand'] = 'CanadianSolar MaxPower CS6U-340M'
            self.pvbrand.setText(str(globals.pv_data['pvbrand']))
            self.pvcap.setText(str(self.pv_models['Capacity'][self.pvbrand.text()]))
            self.PV_Efficiency.setText(str(self.pv_models['Efficiencies'][self.pvbrand.text()]))
            self.Temp_Derating.setText(str(self.pv_models['Coefficient'][self.pvbrand.text()]))
        elif self.pv_config.currentIndex() == 4:
            globals.pv_data['pvbrand'] = 'CanadianSolar MaxPower CS6X-325P'
            self.pvbrand.setText(str(globals.pv_data['pvbrand']))
            self.pvcap.setText(str(self.pv_models['Capacity'][self.pvbrand.text()]))
            self.PV_Efficiency.setText(str(self.pv_models['Efficiencies'][self.pvbrand.text()]))
            self.Temp_Derating.setText(str(self.pv_models['Coefficient'][self.pvbrand.text()]))
        elif self.pv_config.currentIndex() == 5:
            globals.pv_data['pvbrand'] = 'CanadianSolar Quintech CS6K-285M'
            self.pvbrand.setText(str(globals.pv_data['pvbrand']))
            self.pvcap.setText(str(self.pv_models['Capacity'][self.pvbrand.text()]))
            self.PV_Efficiency.setText(str(self.pv_models['Efficiencies'][self.pvbrand.text()]))
            self.Temp_Derating.setText(str(self.pv_models['Coefficient'][self.pvbrand.text()]))
        elif self.pv_config.currentIndex() == 6:
            globals.pv_data['pvbrand'] = 'CanadianSolar SuperPower CS6K-295MS'
            self.pvbrand.setText(str(globals.pv_data['pvbrand']))
            self.pvcap.setText(str(self.pv_models['Capacity'][self.pvbrand.text()]))
            self.PV_Efficiency.setText(str(self.pv_models['Efficiencies'][self.pvbrand.text()]))
            self.Temp_Derating.setText(str(self.pv_models['Coefficient'][self.pvbrand.text()]))
        self.main_window.show_status_message('Solar Panel Data Loaded Successfully')

        globals.longitude = float(self.edit_lon.text())
    
    # Method Updates the Global Inverter Variables with the User Input
    def update_inverter(self):
        if self.inv_config.currentIndex() == 0:
            globals.pv_data['inverter'] = 'CyboEnergy Grid-Interactive C1-Mini-1000A'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 1:
            globals.pv_data['inverter'] = 'CyboEnergy Off-Grid C1-Mini-1000N'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 2:
            globals.pv_data['inverter'] = 'Eaton Power Xpert 1000kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 3:
            globals.pv_data['inverter'] = 'Eaton Power Xpert 1500kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 4:
            globals.pv_data['inverter'] = 'Eaton Power Xpert 2000kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 5:
            globals.pv_data['inverter'] = 'Eaton Power Xpert 2250kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 6:
            globals.pv_data['inverter'] = 'Fronius Symo 20.0-3-M'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 7:
            globals.pv_data['inverter'] = 'Fronius Symo 8.2-3-M'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 8:
            globals.pv_data['inverter'] = 'Fronius Galvo 2.5-1'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 9:
            globals.pv_data['inverter'] = 'Fronius Primo 8.2-1'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 10:
            globals.pv_data['inverter'] = 'Fronius Symo 4.5-3-S'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 11:
            globals.pv_data['inverter'] = 'Leonics MTP-4117H 300kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 12:
            globals.pv_data['inverter'] = 'Leonics MTP-413F 25kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 13:
            globals.pv_data['inverter'] = 'Leonics S-219Cp 5kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 14:
            globals.pv_data['inverter'] = 'Leonics STP-219Cp 15kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 15:
            globals.pv_data['inverter'] = 'Leonics GTP-507 125kW'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        elif self.inv_config.currentIndex() == 16:
            globals.pv_data['inverter'] = 'Magnum MS4448PAE'
            self.Inverter_eff.setText(str(self.inverter_data['Efficiencies'][globals.pv_data['inverter']]))
        self.main_window.show_status_message('Inverter Data Loaded Successfully')
    
    # Refreshes the Data Input Fields with Global Variables  
    def refresh_data(self):
        self.edit_lat.setText(str(globals.latitude))
        self.edit_lon.setText(str(globals.longitude))
        self.edit_addr.setText(str(globals.address))
        self.PV_Efficiency.setText(str(globals.pv_data['PV_eff']))
        self.pvcap.setText(str(globals.pv_data['pvcap']))
        self.pvbrand.setText(str(globals.pv_data['pvbrand']))
        self.Temp_Derating.setText(str(globals.pv_data['P_coeff']))
        self.wiring_eff.setText(str(globals.pv_data['wire_eff']))
        self.PV_Area.setText(str(globals.pv_data['area']))
        self.Inverter_eff.setText(str(globals.pv_data['eff_inv']))
        self.edit_tilt.setText(str(globals.pv_data['tilt']))
    