# This Class Sets Up the Graphical User Interface of the Battery Page 
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuickWidgets, QtPositioning
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import smart.globals as globals
                       
class battery_ui(QWidget): 
    def setup(self, window): 

        self.main_window = window 
        labelFont=QFont("Futura", 20)       
        
        title1 = QLabel('Battery configuration')
        title1.setStyleSheet('color: orange')
        title1.setFont(labelFont)
        
        label1 = QLabel('  Number of batteries:')
        label1.setStyleSheet('color: beige')
        label1.setFixedWidth(200)
        
        self.edit_nBatt = QLineEdit()
        self.edit_nBatt.setFixedWidth(70)
        
        label2a = QLabel('Nominal capacity:')
        label2a.setStyleSheet('color: beige')
        label2b = QLabel('Ah')
        label2b.setStyleSheet('color: beige')
        
        self.edit_Cnom = QLineEdit()
        self.edit_Cnom.setFixedWidth(100)
        
        label3a = QLabel('Nominal voltage:')
        label3a.setFixedWidth(100)
        label3a.setStyleSheet('color: beige')
        label3b = QLabel('Vdc')
        label3b.setStyleSheet('color: beige')
        label3b.setFixedWidth(50)
        
        self.edit_Vdc = QLineEdit()
        self.edit_Vdc.setFixedWidth(100)
        
        title2 = QLabel('Battery discharge characteristics')
        title2.setStyleSheet('color: orange')
        title2.setFont(labelFont)
      
        vline = QFrame()
        vline.setFrameStyle(QFrame.VLine | QFrame.Sunken)
        
        title3 = QLabel('Battery charge parameters')
        title3.setStyleSheet('color: orange')
        title3.setFont(labelFont)
        
        label4a = QLabel('Battery converter / inverter efficiency:')
        label4a.setStyleSheet('color: beige')
        label4b = QLabel('%')
        label4b.setStyleSheet('color: beige')
        
        self.Inverter_effConv = QLineEdit()
        self.Inverter_effConv.setFixedWidth(100)
        
        label5a = QLabel('Battery initial state of charge:')
        label5a.setStyleSheet('color: beige')
        label5b = QLabel('%')
        label5b.setStyleSheet('color: beige')
        
        self.edit_initSOC = QLineEdit()
        self.edit_initSOC.setFixedWidth(100)
        
        label6a = QLabel('Battery minimum state of charge:')
        label6a.setStyleSheet('color: beige')
        label6b = QLabel('%')
        label6b.setStyleSheet('color: beige')
        
        self.edit_minSOC = QLineEdit()
        self.edit_minSOC.setFixedWidth(100)
        
        title4 = QLabel('Battery ramp control parameters')
        title4.setStyleSheet('color: orange')
        title4.setFont(labelFont)
        
        label7a = QLabel('PV output setpoint for ramp control:')
        label7a.setStyleSheet('color: beige')
        label7b = QLabel('W')
        label7b.setStyleSheet('color: beige')
        
        self.edit_Pset = QLineEdit()
        self.edit_Pset.setFixedWidth(100)
        
        label8a = QLabel('Ramp control start time:')
        label8a.setStyleSheet('color: beige')
        label8b = QLabel('hour')
        label8b.setStyleSheet('color: beige')
        
        self.edit_Ton = QLineEdit()
        self.edit_Ton.setFixedWidth(100)
        
        label9a = QLabel('Ramp control stop time:')
        label9b = QLabel('hour')
        label9a.setStyleSheet('color: beige')
        label9b.setStyleSheet('color: beige')
        
        self.edit_Toff = QLineEdit()
        self.edit_Toff.setFixedWidth(100)
        
        label10a = QLabel('Battery Brand')
        label10b = QLabel('%')
        label10a.setStyleSheet('color: beige')
        label10b.setStyleSheet('color: beige')
        
        self.brand = QLineEdit()
        self.brand.setFixedWidth(300)

        batt_label = QLabel('Select a Battery Model')
        batt_label.setStyleSheet('color: orange')
        batt_label.setFont(labelFont)
        self.batt_config = QComboBox()
        self.batt_config.setFixedWidth(300)
        self.batt_config.addItems(['Trojan SAGM 12 75', 
                        'Trojan SAGM 12 90', 
                        'Trojan SAGM 12 105', 
                        'Trojan SIND 02 1990', 
                        'Trojan SIND 02 2450', 
                        'Trojan SIND 04 1685', 
                        'Trojan SIND 04 2145', 
                        'Trojan SIND 06 610', 
                        'Trojan SIND 06 920', 
                        'Trojan SIND 06 1225', 
                        'Trojan SPRE 02 1255', 
                        'Trojan SPRE 06 225', 
                        'Trojan SPRE 06 415', 
                        'Trojan SPRE 12 225', 
                        'Trojan SSIG 06 235', 
                        'Trojan SSIG 06 255'])

        self.batt_config.currentIndexChanged.connect(self.update_battery)
        pixmap = QPixmap('battery.png')
        self.image = QLabel()
        self.image.setPixmap(pixmap)
        self.image.setGeometry(1, 14, 15, 100)

        self.battery_data = {'Voltage': {
                        'Trojan SAGM 12 75': '12', 
                        'Trojan SAGM 12 90': '12', 
                        'Trojan SAGM 12 105': '12', 
                        'Trojan SIND 02 1990': '2', 
                        'Trojan SIND 02 2450': '2', 
                        'Trojan SIND 04 1685': '4', 
                        'Trojan SIND 04 2145': '4', 
                        'Trojan SIND 06 610': '6', 
                        'Trojan SIND 06 920': '6', 
                        'Trojan SIND 06 1225': '6', 
                        'Trojan SPRE 02 1255': '2', 
                        'Trojan SPRE 06 225': '6', 
                        'Trojan SPRE 06 415': '6', 
                        'Trojan SPRE 12 225': '12', 
                        'Trojan SSIG 06 235': '6', 
                        'Trojan SSIG 06 255': '6'
                        },
                'Discharge_Power': {
                        'Trojan SAGM 12 75': '2.28', 
                        'Trojan SAGM 12 90': '2.67', 
                        'Trojan SAGM 12 105': '3.156', 
                        'Trojan SIND 02 1990': '0.6', 
                        'Trojan SIND 02 2450': '0.6', 
                        'Trojan SIND 04 1685': '1.2', 
                        'Trojan SIND 04 2145': '1.2', 
                        'Trojan SIND 06 610': '1.8', 
                        'Trojan SIND 06 920': '1.8', 
                        'Trojan SIND 06 1225': '1.8', 
                        'Trojan SPRE 02 1255': '0.6', 
                        'Trojan SPRE 06 225': '1.8', 
                        'Trojan SPRE 06 415': '1.8', 
                        'Trojan SPRE 12 225': '3.6', 
                        'Trojan SSIG 06 235': '1.8', 
                        'Trojan SSIG 06 255': '1.8'
                        },
                'Capacity': {
                        'Trojan SAGM 12 75': '75.0',
                         'Trojan SAGM 12 90': '90.0', 
                         'Trojan SAGM 12 105': '105.0', 
                         'Trojan SIND 02 1990': '1990.0', 
                         'Trojan SIND 02 2450': '2450.0', 
                         'Trojan SIND 04 1685': '1685.0', 
                         'Trojan SIND 04 2145': '2145.0', 
                         'Trojan SIND 06 610': '610.0', 
                         'Trojan SIND 06 920': '920.0', 
                         'Trojan SIND 06 1225': '1225.0', 
                         'Trojan SPRE 02 1255': '1255.0', 
                         'Trojan SPRE 06 225': '225.0', 
                         'Trojan SPRE 06 415': '415.0', 
                         'Trojan SPRE 12 225': '225.0', 
                         'Trojan SSIG 06 235': '235.0', 
                         'Trojan SSIG 06 255': '255.0'
                        }
                }
        
        layout = QGridLayout()
        layout.addWidget(title1, 0, 8)
        layout.addWidget(label1, 2, 0, 1, 2)
        layout.addWidget(self.edit_nBatt, 2, 2)
        layout.addWidget(label2a, 1, 8)
        layout.addWidget(self.edit_Cnom, 1, 9)
        layout.addWidget(label2b, 1, 10)
        layout.addWidget(label3a, 2, 8)
        layout.addWidget(self.edit_Vdc, 2, 9)
        layout.addWidget(label3b, 2, 10)
        layout.addWidget(vline, 0, 3, 15, 3)
        layout.addWidget(title3, 0, 4)
        layout.addWidget(label4a, 2, 4)
        layout.addWidget(self.Inverter_effConv, 2, 5)
        layout.addWidget(label4b, 2, 6)
        layout.addWidget(label5a, 3, 4)
        layout.addWidget(self.edit_initSOC, 3, 5)
        layout.addWidget(label5b, 3, 6)
        layout.addWidget(batt_label, 0, 0, 1, 3)
        layout.addWidget(self.batt_config, 1, 0, 1, 3)
        layout.addWidget(label6a, 4, 4)
        layout.addWidget(self.edit_minSOC, 4, 5)
        layout.addWidget(label6b, 4, 6)
        layout.addWidget(label10a, 1, 4)
        layout.addWidget(self.brand, 1, 5)
        layout.addWidget(self.image, 11, 5, 5, 15)
        self.setLayout(layout)

        self.refresh_data()  

    # Method Updates the Global Variables
    def update_data(self):
        globals.batt_data['n_batt'] = int(self.edit_nBatt.text())
        globals.batt_data['C_nom'] = float(self.edit_Cnom.text())
        globals.batt_data['v_dc'] = float(self.edit_Vdc.text())
        globals.batt_data['eff_conv'] = float(self.Inverter_effConv.text())
        globals.batt_data['SOC_0'] = float(self.edit_initSOC.text())
        globals.batt_data['SOC_min'] = float(self.edit_minSOC.text())
        globals.batt_data['p_set'] = float(self.edit_Pset.text())
        globals.batt_data['brand'] = str(self.brand.text())
    
    # Method Updates the Global Battery Variable with the User Input 
    def update_battery(self):
        if self.batt_config.currentIndex() == 0:
            globals.batt_data['brand'] = 'Trojan SAGM 12 75'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 1:
            globals.batt_data['brand'] = 'Trojan SAGM 12 90'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 2:
            globals.batt_data['brand'] = 'Trojan SAGM 12 105'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 3:
            globals.batt_data['brand'] = 'Trojan SIND 02 1990'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 4:
            globals.batt_data['brand'] = 'Trojan SIND 02 2450'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 5:
            globals.batt_data['brand'] = 'Trojan SIND 04 1685'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 6:
            globals.batt_data['brand'] = 'Trojan SIND 04 2145'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 7:
            globals.batt_data['brand'] = 'Trojan SIND 06 610'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 8:
            globals.batt_data['brand'] = 'Trojan SIND 06 920'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 9:
            globals.batt_data['brand'] = 'Trojan SIND 06 1225'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 10:
            globals.batt_data['brand'] = 'Trojan SPRE 02 1255'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 11:
            globals.batt_data['brand'] = 'Trojan SPRE 06 225'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 12:
            globals.batt_data['brand'] = 'Trojan SPRE 06 415'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 13:
            globals.batt_data['brand'] = 'Trojan SPRE 12 225'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 14:
            globals.batt_data['brand'] = 'Trojan SSIG 06 235'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        elif self.batt_config.currentIndex() == 15:
            globals.batt_data['brand'] = 'Trojan SSIG 06 255'
            self.brand.setText(str(globals.batt_data['brand']))
            self.edit_Vdc.setText(str(self.battery_data['Voltage'][self.brand.text()]))
            self.edit_Cnom.setText(str(self.battery_data['Capacity'][self.brand.text()]))
        self.main_window.show_status_message('Battery Data Loaded Successfully')
      
    # Refreshes the Data Input Fields with Global Variables      
    def refresh_data(self):
        self.edit_nBatt.setText(str(globals.batt_data['n_batt']))
        self.edit_Cnom.setText(str(globals.batt_data['C_nom']))
        self.edit_Vdc.setText(str(globals.batt_data['v_dc']))
        self.Inverter_effConv.setText(str(globals.batt_data['eff_conv']))
        self.edit_initSOC.setText(str(globals.batt_data['SOC_0']))
        self.edit_minSOC.setText(str(globals.batt_data['SOC_min']))
        self.brand.setText(str(globals.batt_data['brand']))
        self.edit_Pset.setText(str(globals.batt_data['p_set']))
       