# This Class Sets Up the Graphical User Interface of the Generator Page 
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import smart.globals as globals
                     
class gen_ui(QWidget): 
    def setup(self, window):   
        
        self.main_window = window
        labelFont=QFont("Futura", 20)        
        
        title1 = QLabel('Generator configuration')
        title1.setStyleSheet('color: orange')
        title1.setFont(labelFont)
        
        label1 = QLabel('No. generators:')
        label1.setStyleSheet('color: beige')
        self.edit_nGen = QLineEdit()
        self.edit_nGen.setFixedWidth(100)
        
        label2a = QLabel('Nominal capacity:')
        label2b = QLabel('kW')
        label2a.setStyleSheet('color: beige')
        label2b.setStyleSheet('color: beige')
        
        self.edit_Pgen = QLineEdit()
        self.edit_Pgen.setFixedWidth(100)
        
        label3a = QLabel('Minimum generator loading:')
        label3b = QLabel('%')
        label3a.setStyleSheet('color: beige')
        label3b.setStyleSheet('color: beige')
        
        self.edit_Pmin = QLineEdit()
        self.edit_Pmin.setFixedWidth(100)
        
        label4a = QLabel('Specific fuel consumption:')
        label4b = QLabel('litres/kWh')
        label4a.setStyleSheet('color: beige')
        label4b.setStyleSheet('color: beige')
        
        self.edit_sfc = QLineEdit()
        self.edit_sfc.setFixedWidth(100)
        
        label5a = QLabel('Generator Brand')
        label5b = QLabel('% (DC coupled only)')
        label5a.setStyleSheet('color: beige')
        label5b.setStyleSheet('color: beige')
        
        self.brand = QLineEdit()
        self.brand.setFixedWidth(300)

        gen_label = QLabel('Select a Generator Model')
        gen_label.setStyleSheet('color: orange')
        gen_label.setFont(labelFont)
        self.gen_config = QComboBox()
        self.gen_config.setStyle( QStyleFactory.create( "Polyester" ) )
        self.gen_config.addItems(['Generic 10kW Fixed Capacity Genset', 'Generic 25kW Fixed Capacity Genset', 'Generic 50kW Fixed Capacity Genset', 
                        'Generic 100kW Fixed Capacity Genset', 'Generic 500kW Fixed Capacity Genset', 'Generic 1 MW Fixed Capacity Genset'])
        self.gen_config.currentIndexChanged.connect(self.update_gen)

        pixmap = QPixmap('gen.png')
        self.image = QLabel()
        self.image.setPixmap(pixmap)
        self.image.setGeometry(1, 14, 15, 100)

        self.Generator_Data = {'Sizes': {
                        'Generic 10kW Fixed Capacity Genset': '10', 
                        'Generic 25kW Fixed Capacity Genset': '25', 
                        'Generic 50kW Fixed Capacity Genset': '50', 
                        'Generic 100kW Fixed Capacity Genset': '100', 
                        'Generic 500kW Fixed Capacity Genset': '500', 
                        'Generic 1 MW Fixed Capacity Genset': '1000'
                        }
                     }

        layout = QGridLayout()
        layout.addWidget(title1, 0, 4)
        layout.addWidget(label1, 2, 4)
        layout.addWidget(self.edit_nGen, 2, 5)
        layout.addWidget(label2a, 3, 4)
        layout.addWidget(self.edit_Pgen, 3, 5)
        layout.addWidget(label2b, 3, 6)
        layout.addWidget(label3a, 4, 4)
        layout.addWidget(self.edit_Pmin, 4, 5)
        layout.addWidget(label3b, 4, 6)
        layout.addWidget(label4a, 5, 4)
        layout.addWidget(self.edit_sfc, 5, 5)
        layout.addWidget(label4b, 5, 6)
        layout.addWidget(label5a, 1, 4)
        layout.addWidget(self.brand, 1, 5, 1, 3)
        #layout.addWidget(label5b, 5, 2)
        layout.addWidget(gen_label, 0, 0, 1, 3)
        layout.addWidget(self.gen_config, 1, 0, 1, 3)
        layout.addWidget(self.image, 7, 5, 5, 15)
        self.setLayout(layout)
        self.refresh_data()  
    
    # Method Updates the Global Variables
    def update_data(self):
        globals.gen_data['n_gen'] = int(self.edit_nGen.text())
        globals.gen_data['P_gen'] = float(self.edit_Pgen.text())
        globals.gen_data['l_min'] = float(self.edit_Pmin.text())
        globals.gen_data['e_f'] = float(self.edit_sfc.text())
        globals.gen_data['brand'] = str(self.brand.text())
        
    # Method Updates Text Fields with Generator Datasheet
    def update_gen(self):
        if self.gen_config.currentIndex() == 0:
            globals.gen_data['brand'] = 'Generic 10kW Fixed Capacity Genset'
            self.brand.setText(str(globals.gen_data['brand']))
            self.edit_Pgen.setText(str(self.Generator_Data['Sizes'][self.brand.text()]))
        elif self.gen_config.currentIndex() == 1:
            globals.gen_data['brand'] = 'Generic 25kW Fixed Capacity Genset'
            self.brand.setText(str(globals.gen_data['brand']))
            self.edit_Pgen.setText(str(self.Generator_Data['Sizes'][self.brand.text()]))
        elif self.gen_config.currentIndex() == 2:
            globals.gen_data['brand'] = 'Generic 50kW Fixed Capacity Genset'
            self.brand.setText(str(globals.gen_data['brand']))
            self.edit_Pgen.setText(str(self.Generator_Data['Sizes'][self.brand.text()]))
        elif self.gen_config.currentIndex() == 3:
            globals.gen_data['brand'] = 'Generic 100kW Fixed Capacity Genset'
            self.brand.setText(str(globals.gen_data['brand']))
            self.edit_Pgen.setText(str(self.Generator_Data['Sizes'][self.brand.text()]))
        elif self.gen_config.currentIndex() == 4:
            globals.gen_data['brand'] = 'Generic 500kW Fixed Capacity Genset'
            self.brand.setText(str(globals.gen_data['brand']))
            self.edit_Pgen.setText(str(self.Generator_Data['Sizes'][self.brand.text()]))
        elif self.gen_config.currentIndex() == 5:
            globals.gen_data['brand'] = 'Generic 1 MW Fixed Capacity Genset'
            self.brand.setText(str(globals.gen_data['brand']))
            self.edit_Pgen.setText(str(self.Generator_Data['Sizes'][self.brand.text()]))
        self.main_window.show_status_message('Generator Data Loaded Successfully')

    # Refreshes the Data Input Fields with Global Variables            
    def refresh_data(self):
        self.edit_nGen.setText(str(globals.gen_data['n_gen']))
        self.edit_Pgen.setText(str(globals.gen_data['P_gen']))
        self.edit_Pmin.setText(str(globals.gen_data['l_min']))
        self.edit_sfc.setText(str(globals.gen_data['e_f']))
        self.brand.setText(str(globals.gen_data['brand']))