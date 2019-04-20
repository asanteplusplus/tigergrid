# This is the Main Class of the Software: Sets up all the pages 
import os, sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
import webbrowser
import subprocess
import tkinter
from interface.gui_solar import solar_ui
from interface.gui_loads import loads_ui
from interface.gui_battery import battery_ui
from interface.gui_gen import gen_ui
from interface.gui_project import project_ui
from interface.gui_sim import sim_ui
from interface.gui_wind import wind_ui
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import smart.globals as globals

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        globals.init()
        self.initUI()
    # Initializes the page windows
    def initUI(self):
        screenGeometry = QApplication.instance().desktop().screenGeometry() 
        availGeometry = QApplication.instance().desktop().availableGeometry() 
        width, height = availGeometry.width(), availGeometry.height() 
        self.resize(1800, 1125)
        self.centre()
        self.show()
        self.setWindowTitle('TIGERGRID')
        self.setWindowIcon(QIcon('tiger.png')) 
        oImage = QImage("blueb.jpg")
        sImage = oImage.scaled(QSize(width, height))             # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))                     # 10 = Windowrole
        self.setPalette(palette)
        
        """
        Set up TigerGrid Tabs
        """
        tab_widget = QTabWidget()
        tab1 = QWidget()        
        tab2 = QWidget() 
        tab3 = QWidget()
        tab4 = QWidget()
        tab5 = QWidget()
        tab6 = QWidget()
        tab7 = QWidget()
        self.tab_widget = tab_widget
        
        tab_widget.addTab(tab1, "Project")
        tab_widget.addTab(tab2, "Loads")
        tab_widget.addTab(tab3, "Solar PV") 
        tab_widget.addTab(tab4, "Wind Turbine")
        tab_widget.addTab(tab5, "Battery") 
        tab_widget.addTab(tab6, "Generator") 
        tab_widget.addTab(tab7, "Simulation") 
        
        self.page1 = project_ui(tab1)
        self.page2 = loads_ui(tab2)
        self.page3 = solar_ui(tab3)
        self.page4 = wind_ui(tab4)
        self.page5 = battery_ui(tab5)
        self.page6 = gen_ui(tab6)
        self.page7 = sim_ui(tab7)
        
        self.page1.setup(self)
        self.page2.setup(self)
        self.page3.setup(self)
        self.page4.setup(self)
        self.page5.setup(self)
        self.page6.setup(self)
        self.page7.setup(self)
        
        self.pages = [self.page1, self.page2, self.page3, self.page4, self.page5, self.page6]
        download_button = QPushButton("Next")
        download_button.setFixedWidth(100)
        download_button.clicked.connect(self.buttonClicked)

        """
        Actions
        """
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        saveAsAction = QAction("&Save File", self)
        saveAsAction.setShortcut('Ctrl+S')
        saveAsAction.setStatusTip('Save project as')
        saveAsAction.triggered.connect(self.save_as_fn)

        
        aboutAction = QAction('&About TigerGrid', self)
        aboutAction.setStatusTip('About TigerGrid')
        aboutAction.triggered.connect(self.about_dialog)
        
        helpAction = QAction('&User Manual', self)
        helpAction.setShortcut('Ctrl+M')
        helpAction.setStatusTip('User documentation')
        helpAction.triggered.connect(self.user_manual)   
        
        """
        Menubar
        """
        menu_bar = QMenuBar() 
        fileMenu = menu_bar.addMenu('&File')
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        helpMenu = menu_bar.addMenu('&Help')
        helpMenu.addAction(helpAction)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAction)

        """
        Status line.
        """
        self.status_message = QStatusBar()  
        self.status_message.showMessage("Welcome To TigerGrid")      
        vbox = QVBoxLayout()
        vbox.addWidget(menu_bar)
        vbox.addWidget(tab_widget) 
        vbox.addWidget(download_button, 0, Qt.AlignRight)
        vbox.addWidget(self.status_message)        
        self.setLayout(vbox)
        
    def centre(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def buttonClicked(self, tableWidget):
        self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex()+1)
     
    # Refreshes Data Across Pages    
    def refresh_data(self):
        for p in self.pages:
            p.refresh_data()

    # Method to display messages to user
    def show_status_message(self, message, error = False, beep = False):
        if(error):
            self.status_message.setStyleSheet('QStatusBar {color: red}')
        else:
            self.status_message.setStyleSheet('')
        if beep:
            QApplication.beep()
        self.status_message.showMessage(message)
    
    # Save As Action
    def save_as_fn(self):
        try:
            fname, _filter = QFileDialog.getSaveFileName(self, "Save Data File As", "", "TigerGrid project files (*.txt)")
            file = open(fname, "w")
            text = globals.output
            file.write(text)
            file.close()
        except:
            self.show_status_message("Save As cancelled.")          
        
    def save_fn(self):    
        """Function for the Save action."""
        if globals.filename != "":
            if globals.write_project_to_file(globals.filename):                
                self.refresh_data()        
            else:
                self.show_status_message("Failed to save " + globals.filename + ".", error = True, beep = True)
        
    def user_manual(self):
        """Launch user manual (Github link)"""
        url = "https://github.com/asanteplusplus/tigergrid/blob/master/README.md"
        if sys.platform=='win32':
            os.startfile(url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
                print ('Please open a browser on: '+url)
    
    # About dialog box
    def about_dialog(self):
        QMessageBox.about(self, "About TigerGrid",
                """<b>TigerGrid</b> is a hybrid power system simulation package.
                   <p>
                   Version: <b>v1.0<b><p>
                   <p>
                   <p>&copy; 2019 Alexander Asante</p>
                   <p>All rights reserved.</p>  
                   """)
    
def main():
    app = QApplication(sys.argv)
    w = Window()
    #w.show()
    w.showFullScreen() 
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()