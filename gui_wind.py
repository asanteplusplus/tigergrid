# This Class Sets Up the Graphical User Interface of the Wind Turbine Page 
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuickWidgets, QtPositioning
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import smart.globals as globals
                 
class wind_ui(QWidget): 
    def setup(self, window):
        
        self.main_window = window
        labelFont=QFont("Futura", 20) 

        wind_label = QLabel('Wind Turbine Model')
        wind_label.setStyleSheet('color: orange')
        wind_label.setFont(labelFont)
        self.wind_config = QComboBox()
        self.wind_config.setStyle( QStyleFactory.create( "Polyester" ) )
        self.wind_config.addItems(['ACSA A27/225','Acciona AW-70/1500', 'Ennera Energy windera s', 'Gamesa G39 Turbine', 'General Electric GE 1.5sl', 'Greenstorm GS 21 S', 'Nordic Windpower AB Nordic 400'])
        self.wind_config.currentIndexChanged.connect(self.update_brand)

        title1 = QLabel('Wind Energy System')
        title1.setStyleSheet('color: orange')
        title1.setFont(labelFont)

        windbrand_label = QLabel('Wind Turbine Brand:')
        windbrand_label.setStyleSheet('color: beige')
        self.windbrand = QLineEdit()
        self.windbrand.setFixedWidth(300)

        rated_wind_speed_label = QLabel('Rated wind speed:')
        rated_wind_speed_label.setStyleSheet('color: beige')
        rated_wind_speed_unit = QLabel('m/s')
        rated_wind_speed_unit.setStyleSheet('color: beige')
        self.rated_wind_speed = QLineEdit()
        self.rated_wind_speed.setFixedWidth(100)

        turbine_cap_label = QLabel('Wind Turbine Capacity:')
        turbine_cap_label.setStyleSheet('color: beige')
        turbine_cap_unit = QLabel('kW')
        turbine_cap_unit.setStyleSheet('color: beige')
        self.turbine_cap = QLineEdit()
        self.turbine_cap.setFixedWidth(100)

        blade_len_label = QLabel('Blade Length:')
        blade_len_label.setStyleSheet('color: beige')
        blade_len_unit = QLabel('metre')
        blade_len_unit.setStyleSheet('color: beige')
        self.blade_len = QLineEdit()
        self.blade_len.setFixedWidth(100)

        area_label = QLabel('Area:')
        area_label.setStyleSheet('color: beige')
        area_unit = QLabel('Square Metres')
        area_unit.setStyleSheet('color: beige')
        self.area = QLineEdit()
        self.area.setFixedWidth(100)

        P_eff_label = QLabel('Power Efficiency:')
        P_eff_label.setStyleSheet('color: beige')
        P_eff_unit = QLabel('')
        P_eff_unit.setStyleSheet('color: beige')
        self.P_eff = QLineEdit()
        self.P_eff.setFixedWidth(100)

        hub_height_label = QLabel('Hub Height:')
        hub_height_label.setStyleSheet('color: beige')
        hub_height_unit = QLabel('Square Metre')
        hub_height_unit.setStyleSheet('color: beige')
        self.hub_height = QLineEdit()
        self.hub_height.setFixedWidth(100)

        title2 = QLabel('Meteorological Conditions')
        title2.setStyleSheet('color: orange')
        title2.setFont(labelFont)

        air_density_label = QLabel('Air Density:')
        air_density_label.setStyleSheet('color: beige')
        air_density_unit = QLabel('Kilogram per cubic metre')
        air_density_unit.setStyleSheet('color: beige')
        self.air_density = QLineEdit()
        self.air_density.setFixedWidth(100)

        self.wind_models =     {
                'Capacity': {
                        'ACSA A27/225': '225.0', 
                        'Acciona AW-70/1500': '1500.0', 
                        'Ennera Energy windera s': '3.2', 
                        'Gamesa G39 Turbine': '500.0', 
                        'General Electric GE 1.5sl': '1500.0', 
                        'Greenstorm GS 21 S': '60.0', 
                        'Nordic Windpower AB Nordic 400': '400.0 '
                        },
                'Length': {
                        'ACSA A27/225': '13.5', 
                        'Acciona AW-70/1500': '35', 
                        'Ennera Energy windera s': '2.2', 
                        'Gamesa G39 Turbine': '19.5', 
                        'General Electric GE 1.5sl': '38.5', 
                        'Greenstorm GS 21 S': '11.15', 
                        'Nordic Windpower AB Nordic 400': '17.7'
                        },
                'Area': {
                        'ACSA A27/225': '573.0', 
                        'Acciona AW-70/1500': '3848.0', 
                        'Ennera Energy windera s': '14.9', 
                        'Gamesa G39 Turbine': '1195.0', 
                        'General Electric GE 1.5sl': '4657.0', 
                        'Greenstorm GS 21 S': '386.7', 
                        'Nordic Windpower AB Nordic 400': '984.0' 
                        },
                'Height': {
                        'ACSA A27/225': '30', 
                        'Acciona AW-70/1500': '60', 
                        'Ennera Energy windera s': '12', 
                        'Gamesa G39 Turbine': '40.5', 
                        'General Electric GE 1.5sl': '80.0', 
                        'Greenstorm GS 21 S': '36.0', 
                        'Nordic Windpower AB Nordic 400': '40.0'
                        },
                'Wind_Speed': {
                        'ACSA A27/225': '13.5', 
                        'Acciona AW-70/1500': '11.6', 
                        'Ennera Energy windera s': '11.0', 
                        'Gamesa G39 Turbine': '15.0', 
                        'General Electric GE 1.5sl': '12.0', 
                        'Greenstorm GS 21 S': '8.8', 
                        'Nordic Windpower AB Nordic 400': '14.0'
                        }
                }

        pixmap = QPixmap('windphoto.png')
        self.image = QLabel()
        self.image.setPixmap(pixmap)
        self.image.setGeometry(1, 14, 15, 100)

        layout = QGridLayout()
        layout.addWidget(title1, 0, 5, 1, 3)
        layout.addWidget(wind_label, 0, 0)
        layout.addWidget(self.wind_config, 1, 0)
        layout.addWidget(windbrand_label, 1, 5)
        layout.addWidget(self.windbrand, 1, 6, 1, 3)
        layout.addWidget(rated_wind_speed_label, 2, 5)
        layout.addWidget(rated_wind_speed_unit, 2, 7)
        layout.addWidget(self.rated_wind_speed, 2, 6)
        layout.addWidget(turbine_cap_label, 3, 5)
        layout.addWidget(turbine_cap_unit, 3, 7)
        layout.addWidget(self.turbine_cap, 3, 6)
        layout.addWidget(blade_len_label, 4, 5)
        layout.addWidget(blade_len_unit, 4, 7)
        layout.addWidget(self.blade_len, 4, 6)
        layout.addWidget(area_label, 5, 5)
        layout.addWidget(area_unit, 5, 7)
        layout.addWidget(self.area, 5, 6)
        layout.addWidget(P_eff_label, 6, 5)
        layout.addWidget(P_eff_unit, 6, 7)
        layout.addWidget(self.P_eff, 6, 6)
        layout.addWidget(hub_height_label, 7, 5)
        layout.addWidget(hub_height_unit, 7, 7)
        layout.addWidget(self.hub_height, 7, 6)
        layout.addWidget(air_density_label, 8, 5)
        layout.addWidget(air_density_unit, 8, 7)
        layout.addWidget(self.air_density , 8, 6)
        layout.addWidget(self.image, 11, 11, 5, 15)
        self.setLayout(layout)
        
        self.refresh_data()

    # Method Updates the Global Wind Variables with the User Input      
    def update_brand(self):
        """Update global variables to match GUI fields"""
        if self.wind_config.currentIndex() == 0:
            globals.wind_data['brand'] = 'ACSA A27/225'
            self.windbrand.setText(str(globals.wind_data['brand']))
            self.turbine_cap.setText(str(self.wind_models['Capacity'][self.windbrand.text()]))
            self.area.setText(str(self.wind_models['Area'][self.windbrand.text()]))
            self.blade_len.setText(str(self.wind_models['Length'][self.windbrand.text()]))
            self.hub_height.setText(str(self.wind_models['Height'][self.windbrand.text()]))
            self.rated_wind_speed.setText(str(self.wind_models['Wind_Speed'][self.windbrand.text()]))

        elif self.wind_config.currentIndex() == 1:
            globals.wind_data['brand'] = 'Acciona AW-70/1500'
            self.windbrand.setText(str(globals.wind_data['brand']))
            self.turbine_cap.setText(str(self.wind_models['Capacity'][self.windbrand.text()]))
            self.area.setText(str(self.wind_models['Area'][self.windbrand.text()]))
            self.blade_len.setText(str(self.wind_models['Length'][self.windbrand.text()]))
            self.hub_height.setText(str(self.wind_models['Height'][self.windbrand.text()]))
            self.rated_wind_speed.setText(str(self.wind_models['Wind_Speed'][self.windbrand.text()]))
        elif self.wind_config.currentIndex() == 2:
            globals.wind_data['brand'] = 'Ennera Energy windera s'
            self.windbrand.setText(str(globals.wind_data['brand']))
            self.turbine_cap.setText(str(self.wind_models['Capacity'][self.windbrand.text()]))
            self.area.setText(str(self.wind_models['Area'][self.windbrand.text()]))
            self.blade_len.setText(str(self.wind_models['Length'][self.windbrand.text()]))
            self.hub_height.setText(str(self.wind_models['Height'][self.windbrand.text()]))
            self.rated_wind_speed.setText(str(self.wind_models['Wind_Speed'][self.windbrand.text()]))
        elif self.wind_config.currentIndex() == 3:
            globals.wind_data['brand'] = 'Gamesa G39 Turbine'
            self.windbrand.setText(str(globals.wind_data['brand']))
            self.turbine_cap.setText(str(self.wind_models['Capacity'][self.windbrand.text()]))
            self.area.setText(str(self.wind_models['Area'][self.windbrand.text()]))
            self.blade_len.setText(str(self.wind_models['Length'][self.windbrand.text()]))
            self.hub_height.setText(str(self.wind_models['Height'][self.windbrand.text()]))
            self.rated_wind_speed.setText(str(self.wind_models['Wind_Speed'][self.windbrand.text()]))
        elif self.wind_config.currentIndex() == 4:
            globals.wind_data['brand'] = 'General Electric GE 1.5sl'
            self.windbrand.setText(str(globals.wind_data['brand']))
            self.turbine_cap.setText(str(self.wind_models['Capacity'][self.windbrand.text()]))
            self.area.setText(str(self.wind_models['Area'][self.windbrand.text()]))
            self.blade_len.setText(str(self.wind_models['Length'][self.windbrand.text()]))
            self.hub_height.setText(str(self.wind_models['Height'][self.windbrand.text()]))
            self.rated_wind_speed.setText(str(self.wind_models['Wind_Speed'][self.windbrand.text()]))
        elif self.wind_config.currentIndex() == 5:
            globals.wind_data['brand'] = 'Greenstorm GS 21 S'
            self.windbrand.setText(str(globals.wind_data['brand']))
            self.turbine_cap.setText(str(self.wind_models['Capacity'][self.windbrand.text()]))
            self.area.setText(str(self.wind_models['Area'][self.windbrand.text()]))
            self.blade_len.setText(str(self.wind_models['Length'][self.windbrand.text()]))
            self.hub_height.setText(str(self.wind_models['Height'][self.windbrand.text()]))
            self.rated_wind_speed.setText(str(self.wind_models['Wind_Speed'][self.windbrand.text()]))
        elif self.wind_config.currentIndex() == 6:
            globals.wind_data['brand'] = 'Nordic Windpower AB Nordic 400'
            self.windbrand.setText(str(globals.wind_data['brand']))
            self.turbine_cap.setText(str(self.wind_models['Capacity'][self.windbrand.text()]))
            self.area.setText(str(self.wind_models['Area'][self.windbrand.text()]))
            self.blade_len.setText(str(self.wind_models['Length'][self.windbrand.text()]))
            self.hub_height.setText(str(self.wind_models['Height'][self.windbrand.text()]))
            self.rated_wind_speed.setText(str(self.wind_models['Wind_Speed'][self.windbrand.text()]))
        self.main_window.show_status_message('Wind Turbine Data Loaded Successfully')

    # Method Updates the Global Variables
    def update_data(self):
        globals.wind_data['P_eff'] = float(self.P_eff.text())
        globals.wind_data['rated_wind_speed'] = float(self.rated_wind_speed.text())
        globals.wind_data['blade_length'] = float(self.blade_len.text())
        globals.wind_data['area'] = float(self.area.text())
        globals.wind_data['hub_height'] = float(self.hub_height.text())
        globals.wind_data['air_density'] = float(self.air_density.text())
        globals.wind_data['cap'] = float(self.turbine_cap.text())
        globals.wind_data['brand'] = str(self.windbrand.text())

    # Refreshes the Data Input Fields with Global Variables
    def refresh_data(self):
        self.P_eff.setText(str(globals.wind_data['P_eff']))
        self.rated_wind_speed.setText(str(globals.wind_data['rated_wind_speed']))
        self.blade_len.setText(str(globals.wind_data['blade_length']))
        self.area.setText(str(globals.wind_data['area']))
        self.hub_height.setText(str(globals.wind_data['hub_height']))
        self.air_density.setText(str(globals.wind_data['air_density']))
        self.turbine_cap.setText(str(globals.wind_data['cap']))
        self.windbrand.setText(str(globals.wind_data['brand']))
        