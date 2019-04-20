# This Class Sets Up the Graphical User Interface of the Simulation Page  
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import statistics
import numpy as np
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import smart.globals as globals
from smart.chron_sim import run_sim
                    
class sim_ui(QWidget): 
    def setup(self, window):   
        
        self.main_window = window
        labelFont=QFont("Segoe UI", 20)        
        
        run_button = QPushButton("Simulate Current System Design")
        run_button.setFixedWidth(300)
        
        title1 = QLabel('Output Window')
        title1.setStyleSheet('color: orange')
        title1.setFont(labelFont)

        optLabel = QLabel('Alternatively, Use the AutoSize Optimizer')
        optLabel.setStyleSheet('color: orange')
        optLabel.setFont(labelFont)
        space = QLabel('  ')
        space.setFont(labelFont)

        instr_label = QLabel('Input the Percentage of your Power Supply that you want from the Following Components Below')
        instr_label.setStyleSheet('color: beige')
        instr_label.setFont(QFont("Futura", 12))
        instr2_label = QLabel('')
        instr2_label.setStyleSheet('color: beige')

        solar_label = QLabel('Solar:')
        solar_label.setStyleSheet('color: orange')
        solar_unit = QLabel('%')
        solar_unit.setStyleSheet('color: orange')
        self.solar = QLineEdit()
        self.solar.setFixedWidth(100)
        self.solar.setPlaceholderText("25")

        wind_label = QLabel('Wind:')
        wind_label.setStyleSheet('color: orange')
        wind_unit = QLabel('%')
        wind_unit.setStyleSheet('color: orange')
        self.wind = QLineEdit()
        self.wind.setFixedWidth(100)
        self.wind.setPlaceholderText("25")

        batt_label = QLabel('Battery:')
        batt_label.setStyleSheet('color: orange')
        batt_unit = QLabel('%')
        batt_unit.setStyleSheet('color: orange')
        self.batt = QLineEdit()
        self.batt.setFixedWidth(100)
        self.batt.setPlaceholderText("25")

        gen_label = QLabel('Generator:')
        gen_label.setStyleSheet('color: orange')
        gen_unit = QLabel('%')
        gen_unit.setStyleSheet('color: orange')
        self.gen = QLineEdit()
        self.gen.setFixedWidth(100)
        self.gen.setPlaceholderText("25")

        self.opt_button = QPushButton("Run AutoSize Optimizer")
        self.opt_button.setFixedWidth(260)
        self.opt_button.clicked.connect(self.button_opt)
        
        clear_button = QPushButton("Clear")
        clear_button.setFixedWidth(80)

        space = QLabel('                  ')
        space.setFont(labelFont)
        space.setFixedWidth(10)
        
        font = QFont("Futura", 15)
        self.textBox = QTextEdit()
        self.textBox.setReadOnly(True)
        self.textBox.setFont(font)
        self.textBox.setMinimumSize(QtCore.QSize(1000,600))
        
        title2 = QLabel('Plot Outputs')
        title2.setStyleSheet('color: orange')
        title2.setFont(labelFont)
        
        self.combo_plot = QComboBox()
        self.combo_plot.setStyle( QStyleFactory.create( "Polyester" ) )
        self.combo_plot.setFixedWidth(150)
        plot_button = QPushButton("Plot")

        pixmap = QPixmap('tigergrid.png')
        self.image = QLabel()
        self.image.setPixmap(pixmap)
        
        layout = QGridLayout()
        layout.addWidget(run_button, 0, 1, 2, 2)
        layout.addWidget(title1, 1, 1)
        layout.addWidget(optLabel, 1, 11, 1, 4)
        layout.addWidget(instr_label, 2, 11, 1, 4)
        layout.addWidget(clear_button, 1, 2)
        layout.addWidget(space, 3, 10)
        layout.addWidget(self.textBox, 2, 1, 5, 9)
        layout.addWidget(title2, 7, 1)
        layout.addWidget(self.combo_plot, 8, 1)
        layout.addWidget(plot_button, 8, 2)
        layout.addWidget(self.image, 0, 11, 1, 4)
        layout.addWidget(solar_label, 3, 11)
        layout.addWidget(solar_unit, 3, 13)
        layout.addWidget(self.solar, 3, 12)
        layout.addWidget(wind_label, 4, 11)
        layout.addWidget(wind_unit, 4, 13)
        layout.addWidget(self.wind, 4, 12)
        layout.addWidget(batt_label, 5, 11)
        layout.addWidget(batt_unit, 5, 13)
        layout.addWidget(self.batt, 5, 12)
        layout.addWidget(gen_label, 6, 11)
        layout.addWidget(gen_unit, 6, 13)
        layout.addWidget(self.gen, 6, 12)
        layout.addWidget(self.opt_button, 7, 11, 2, 4)
        self.setLayout(layout)

        run_button.clicked.connect(self.runBtnClicked)
        clear_button.clicked.connect(self.clear_fn)
        plot_button.clicked.connect(self.plotBtnClicked)
        
        # Clear output window
        self.textBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.textBox.customContextMenuRequested.connect(self.textbox_menu)
    
    # Updates the textbox for the output window
    def textbox_menu(self, point):
        menu = self.textBox.createStandardContextMenu(point)
        clearLog = QAction('Clear output window', self)
        clearLog.setStatusTip('Clear output window')
        clearLog.triggered.connect(self.clear_fn)
        
        menu.addAction(clearLog)
        menu.exec_(self.textBox.viewport().mapToGlobal(point))
    
    # Writes to the output window
    def write(self, msg):
        font = QFont("Futura", 15)
        self.textBox.setFont(font)
        self.textBox.insertPlainText(str(msg))
    
    # Clears the output window
    def clear_fn(self):
        self.textBox.clear()

    # Runs the Autosize optimizer    
    def button_opt(self):
        print("Optimizer Button Clicked")
        globals.optimizer = True
        print(globals.optimizer)
        globals.opt_solar = self.solar.text()
        globals.opt_wind = self.wind.text()
        globals.opt_batt = self.batt.text()
        globals.opt_gen = self.gen.text()
        if str((float(self.solar.text())+float(self.wind.text())+float(self.batt.text())+float(self.gen.text()))) != str(100.0):
            self.main_window.show_status_message('Error: Sum of Percentages must Equal 100')
        else:
            self.main_window.show_status_message('Running Simulation ...')
            globals.sys_data['is_pv'] = True
            globals.sys_data['is_batt'] = True
            globals.sys_data['is_gen'] = True
            globals.sys_data['is_wind'] = True
            print('Solar Size ' + str(globals.opt_solar))
            print(type(self.solar.text()))
            self.runBtnClicked()

    # Method for plotting output graphs
    def plotBtnClicked(self):
        """ Plot result outputs """
        if plt.fignum_exists(1):
            # Do nothing if a plot is already open
            QMessageBox.warning(self, 'Warning', "A plot is already open. Please close to create a new plot.", QMessageBox.Ok)
        else:
            if self.combo_plot.currentText() == 'Solar PV Output':
                q = self.sim_out['G0']
                self.main_window.show_status_message('Generating plot...')
                try:
                    plt.title('Global Horizontal Irradiation for Selected Duration (GHI)')
                    plt.plot(q)
                    plt.ylabel('GHI (KWh/m^2/day)')
                    plt.xlabel('Duration')
                    plt.show()
                except:
                    self.main_window.show_status_message('Plot Window Closed...')
                    plt.close()

            elif self.combo_plot.currentText() == 'Wind Speed':
                q = self.sim_out['speed']
                self.main_window.show_status_message('Generating plot...')
                try:
                    plt.title('Wind Speed at ' + str(self.wind_point) + ' metres for Selected Duration')
                    plt.plot(q)
                    plt.ylabel('Velocity (m/s)')
                    plt.xlabel('Duration')
                    plt.show()
                except:
                    self.main_window.show_status_message('Plot Window Closed...')
                    plt.close()
            else: self.main_window.show_status_message('Error opening plot...')
    
    # Method for simulating designed hybrid energy system
    def runBtnClicked(self):
        self.write('Running simulation...\n')
        self.main_window.show_status_message('DOWNLOADING DATA FROM NASA DATABASE ...')
        
        for p in self.main_window.pages:
            p.update_data()

        # Corner case: Duration of Zero Selected
        print(globals.duration)
        print(type(globals.duration))
        if globals.duration == 0:
            self.main_window.show_status_message('Error: Project Duration Less than one day')
            self.write('Error: Project Duration Less than one day. Go to Project page and select a start and end date\n')
            return

        # Build up input dictionaries from global data
        pv_dict = globals.pv_data
        pv_dict['area'] = globals.pv_data['area']
        pv_dict['wire_eff'] = globals.pv_data['wire_eff'] 
        pv_dict['eff_inv'] = globals.pv_data['eff_inv'] 
        pv_dict['PV_eff'] = globals.pv_data['PV_eff'] 
        batt_dict = globals.batt_data
        batt_dict['eff_conv'] = globals.batt_data['eff_conv'] 
        gen_dict = globals.gen_data
        gen_dict['l_min'] = globals.gen_data['l_min'] 
        wind_dict = globals.wind_data
        wind_dict['P_eff'] = globals.wind_data['P_eff']
        wind_dict['blade_length'] = globals.wind_data['blade_length']
        wind_dict['area'] = globals.wind_data['area']
        wind_dict['hub_height'] = globals.wind_data['hub_height']
        wind_dict['air_density'] = globals.wind_data['air_density']
        wind_dict['cap'] = globals.wind_data['cap']
        wind_dict['brand'] = globals.wind_data['brand']
        self.combo_plot.clear()
        
        sys_dict = globals.sys_data
        sys_dict['lat'] = globals.latitude
        if sys_dict['is_wind'] == True:
            self.combo_plot.addItem('Wind Speed')
        if sys_dict['is_pv'] == True:
            self.combo_plot.addItem('Solar PV Output')
        self.sim_out = run_sim(sys_dict,pv_dict,batt_dict,gen_dict,wind_dict)
        self.wind_point = 50
        if wind_dict['hub_height'] < 25:
            self.wind_point = 10

        topo = self.sim_out['topo']
        P_ld = self.sim_out['P_ld']
        Wind_Velocity = self.sim_out['speed']
        G0   = self.sim_out['G0']
        P_pv = self.sim_out['P_pv']
        P_wind = self.sim_out['P_wind']
        batt_power = self.sim_out['batt_power']
        batt_hours = self.sim_out['batt_hours']
        P_gen = self.sim_out['P_gen']
        P_gen_xs = self.sim_out['P_gen_xs']
        P_uns = self.sim_out['P_uns']
        P_pv_exc = self.sim_out['P_pv_exc']
        E_tot = float(globals.load_kwhd)*(globals.duration + 1)*(1000.0/24.0)
        
        self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
        self.write('PROJECT INFORMATION \n'.rjust(100))
        self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
        self.write('PROJECT TITLE \n')
        self.write(str(globals.sys_data['proj_title']) + '\n')
        self.write('       '+'\n')
        self.write('PROJECT DESCRIPTION \n')
        self.write(str(globals.sys_data['proj_desc']) + '\n')


        if globals.optimizer == True:
            self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            self.write('RECOMMENDED SIZES FOR SYSTEM DESIGN COMPONENTS \n'.rjust(100))
            self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            if self.solar.text() != str(0):
                self.write('SOLAR PHOTOVOLTAIC \n')
                self.write('Recommended Solar Panel Area: ' + str(round(self.sim_out['opt_area'], 5)) + ' Square metres\n')
            if self.wind.text() != str(0):
                self.write('WIND TURBINE \n')
                self.write('Recommended Wind Turbine Swept Area: ' + str(round(self.sim_out['wind_area'], 5)) + ' Square metres\n')
            if self.batt.text() != str(0):
                self.write('BATTERY \n')
                self.write('Recommended Battery Energy: ' + str(round(self.sim_out['opt_wh'], 5)) + ' watt hours\n')
            if self.gen.text() != str(0):
                self.write('GENERATOR \n')
                self.write('Recommended Generator Rating: ' + str(round(self.sim_out['opt_gen'], 5)) + ' kiloWatts\n')
        
        else:
            self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            self.write('SYSTEM SUMMARY\n'.rjust(95))
            self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            self.write("{:<55}{:25}{:^20}\n".format("Selected Components: ", topo[1], " "))

            if sys_dict['is_pv'] == True:
                self.write("{:<57}{:5}{:^2}\n".format("Solar Panel Brand:  ", str(globals.pv_data['pvbrand']), " "))
                self.write("{:<53}{:5}{:^2}\n".format('Efficiency of the Solar Panel (η): ', str(globals.pv_data['PV_eff']), " "))
                self.write("{:<52}{:5}{:^2}\n".format('PV Temperature Coefficient : ', str(globals.pv_data['P_coeff']), ' %/°C'))
                self.write("{:<57}{:5}{:^2}\n".format('Solar Panel Area: ', str(globals.pv_data['area']), '  metres'))
                self.write("{:<54}{:5}{:^2}\n".format('Solar PV system capacity: ', str(globals.pv_data['pvcap']), ' kiloWatts'))
                self.write("{:<59}{:5}{:^2}\n".format('Inverter Brand: ', str(globals.pv_data['inverter']), " "))
                self.write("{:<56}{:5}{:^2}\n".format('Efficiency of the Inverter (η): ', str(globals.pv_data['eff_inv']), " "))
                self.write('       '+'\n')
            if sys_dict['is_wind'] == True:
                self.write("{:<55}{:5}{:^2}\n".format('Wind Turbine Brand: ', str(globals.wind_data['brand']), " "))
                self.write("{:<48}{:5}{:^2}\n".format('The Swept Area of the wind turbine: ', str(globals.wind_data['area']), ' Square metres'))
                self.write("{:<48}{:5}{:^2}\n".format('The Height of the Wind turbine hub : ', str(globals.wind_data['hub_height']), ' metres'))
                self.write("{:<48}{:5}{:^2}\n".format('The density of the air around the turbine : ', str(globals.wind_data['air_density']), '  Kilogram per cubic metres'))
                self.write("{:<50}{:5}{:^2}\n".format('Power efficiency of the wind turbine: ', str(globals.wind_data['P_eff']), ' (Betz limit = 0.59)'))
                self.write('       '+'\n')
            if sys_dict['is_batt'] == True:
                self.write('Battery Brand: ' + str(globals.batt_data['brand']) + '\n')
                self.write('Nominal Capacity: ' + str(globals.batt_data['C_nom']) + ' Ah\n')
                self.write('Nominal DC Voltage : ' + str(globals.batt_data['v_dc']) + ' V\n')
                self.write('Initial state of charge : ' + str(globals.batt_data['C_nom']*globals.batt_data['SOC_0']) + ' Ah\n')
                self.write('Number of Batteries: ' + str(globals.batt_data['n_batt']) + '\n')
                self.write('       '+'\n')
            if sys_dict['is_gen'] == True:
                self.write("{:<56}{:5}{:^2}\n".format('Generator Brand: ', str(globals.gen_data['brand']), " "))
                self.write("{:<52}{:5}{:^2}\n".format('Generator Rated Capacity: ', str(P_gen), ' kiloWatts'))
                self.write("{:<53}{:5}{:^2}\n".format('Number of Generators: ', str(globals.gen_data['n_gen']), " "))
                self.write('       '+'\n')
            self.write('\n')

            self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            self.write('SIMULATION RESULTS\n'.rjust(95))
            self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            self.write('SYSTEM LOAD \n')
            self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            self.write('Average Load: ' + str(globals.load_kwhd) + ' KWh/d\n')
            self.write('Irradiation days/duration: ' + str(globals.duration + 1) + ' days\n')
            self.write('Total energy demand: ' + str(round(E_tot)) + ' Watts\n')
            self.write('This energy demand is equivalent to: ' + str(E_tot*(24.0/1000.0)) + ' KWh/d\n')
            self.write('Power unsupplied: ' + str(round(P_uns*(24.0/1000.0))) + ' kWh/d (' + str(round((P_uns/E_tot) *100)) + '% of overall demand)\n')
            if P_uns == 0:
                self.write('Primary load demand was met by the current design configuration \n')
            if sys_dict['is_pv'] == True:
                self.write('\n')
                self.write('SOLAR PV SYSTEM \n')
                self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                self.write('Total GHI for duration between dates selected: ' + str(round(sum(G0))) + ' kWh/m2/day\n')
                self.write('Total solar PV system output: ' + str(round(P_pv)) + ' kWh/day\n')
                self.write('Excess solar PV energy: ' + str(round(P_pv_exc)) + ' Watts (' + str(round((P_pv_exc/(P_pv*(1000/24)))*100)) + '% of total solar output)\n')

            if sys_dict['is_wind'] == True:
                self.write('\n')
                self.write('WIND TURBINE SYSTEM \n')
                self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                self.write('Total Energy Generated from wind: ' + str(round(P_wind)) + ' kWh/day\n')
                self.write('Average Wind Speed for given duration: ' + str(statistics.mean(Wind_Velocity)) + ' metres per second\n')

            if sys_dict['is_batt'] == True:
                self.write('\n')
                self.write('BATTERY SYSTEM \n')
                self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                self.write('At the end of the duration, the energy of the battery was : ' + str(round(batt_power)) + ' Watt hours\n')
                # Battery was discharged n-times and recharged m-times by the photovoltaic system
            if sys_dict['is_gen'] == True:
                self.write('\n')
                self.write('GENERATOR \n')
                self.write('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                self.write('Total generator power used to meet primary load over the duration: ' + str(round(P_gen)) + ' Watts \n')
                self.write('Excess generator output after serving load: ' + str(round(P_gen_xs)) + ' Watts \n')
                self.write('Total fuel used by generator over duration: ' + str(round(globals.gen_data['e_f']*24*1000*(P_gen), 3)) + ' Litres \n')


        globals.optimizer = False
        globals.output = self.textBox.toPlainText()
        print(globals.sys_data['is_wind'])
        print(globals.sys_data['is_pv'])
        print(globals.sys_data['is_batt'])
        print(globals.sys_data['is_gen'])
        self.main_window.show_status_message('Simulation complete...')
    
    