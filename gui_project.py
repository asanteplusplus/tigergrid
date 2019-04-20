# This Class Sets Up the Graphical User Interface of the Project Page 
from PyQt5 import QtGui, QtCore, QtWidgets, QtQuickWidgets, QtPositioning
import os
import certifi
import geopy
import ssl
from geopy.geocoders import Nominatim
from interface.gui_loads import loads_ui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import smart.globals as globals

class MarkerObject(QtCore.QObject):
    coordinateChanged = QtCore.pyqtSignal(QtPositioning.QGeoCoordinate)
    sourceChanged = QtCore.pyqtSignal(QtCore.QUrl)

    def __init__(self, parent=None):
        super(MarkerObject, self).__init__(parent)
        self._coordinate = QtPositioning.QGeoCoordinate()
        self._source = QtCore.QUrl()

    def getCoordinate(self):
        return self._coordinate

    def setCoordinate(self, coordinate):
        if self._coordinate != coordinate:
            self._coordinate = coordinate
            self.coordinateChanged.emit(self._coordinate)

    def getSource(self):
        return self._source

    def setSource(self, source):
        if self._source != source:
            self._source = source
            self.sourceChanged.emit(self._source)

    coordinate = QtCore.pyqtProperty(QtPositioning.QGeoCoordinate, fget=getCoordinate, fset=setCoordinate, notify=coordinateChanged)
    source = QtCore.pyqtProperty(QtCore.QUrl, fget=getSource, fset=setSource, notify=sourceChanged)


class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self, parent=None):
        super(MapWidget, self).__init__(parent,
            resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self._marker_object = MarkerObject(parent)
        self._marker_object.setSource(QtCore.QUrl("http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"))
        self.rootContext().setContextProperty("marker_object", self._marker_object)
        #qml_path = os.path.join(os.path.dirname(__file__), "main.qml")
        self.setSource(QtCore.QUrl.fromLocalFile("main.qml"))

    @QtCore.pyqtSlot(QtPositioning.QGeoCoordinate)
    def moveMarker(self, pos):
        self._marker_object.setCoordinate(pos)
                    
class project_ui(QWidget):
    def setup(self, window):
        
        self.main_window = window 
        labelFont=QFont("Futura", 18)      
        
        title1 = QLabel('Project information')
        title1.setStyleSheet('color: orange')
        title1.setFont(QFont("Futura", 20))

        maptitle = QLabel('Location Map')
        maptitle.setStyleSheet('color: orange')
        maptitle.setFont(labelFont)
        
        label1 = QLabel('Title:')
        label1.setStyleSheet('color: orange')
        label1.setFont(labelFont)
        self.edit_title = QLineEdit()
        self.edit_title.setFixedWidth(300)
        
        label2 = QLabel('Description:')
        label2.setStyleSheet('color: orange')
        label2.setFont(labelFont)
        self.edit_desc = QTextEdit()
        self.edit_desc.setFixedWidth(300)

        space = QLabel('                  ')
        space.setFont(labelFont)
        
        title2 = QLabel('System setup')
        title2.setStyleSheet('color: orange')
        title2.setFont(labelFont)

        locAddr = QLabel('Location Address')
        locAddr.setStyleSheet('color: orange')
        locAddr.setFont(labelFont)
        
        label3 = QLabel('    Select System Components Below:')
        label3.setStyleSheet('color: orange')
        label3.setFont(labelFont)
        self.combo_config = QComboBox()
        self.combo_config.addItems(["Genset","PV-Genset","PV-Battery","PV-Battery-Genset"])

        pixmap = QPixmap('tigergrid.png')
        self.image = QLabel()
        self.image.setPixmap(pixmap)
       
        self.lat_value = globals.latitude
        self.lon_value = globals.longitude

        search_button = QtWidgets.QPushButton("Search", clicked=self.search)
        search_button.setFixedWidth(100)
        self._map_widget = MapWidget()
        
        # Location Edit
        self.text_name = QLineEdit(self)
        self.text_name.setFixedWidth(400)
        self.text_name.setPlaceholderText("Address of your Primary Load")
        self.text_name.setText("Accra")

        # Solar Button
        self.solar_button = QPushButton()
        self.solar_button.setFixedWidth(120)
        solar_icon  = QPixmap('solaricon.png')
        self.solar_button.setIcon(QIcon(solar_icon))
        self.solar_button.setIconSize(QSize(200,40))
        self.solar_button.setStyleSheet("background-color: white")
        self.solar_button.setCheckable(True)
        self.solar_button.clicked.connect(self.button_solar)

        # Wind Button
        self.wind_button = QPushButton()
        self.wind_button.setFixedWidth(120)
        wind_icon  = QPixmap('windicon.png')
        self.wind_button.setIcon(QIcon(wind_icon))
        self.wind_button.setIconSize(QSize(200,40))
        self.wind_button.setStyleSheet("background-color: white")
        self.wind_button.setCheckable(True)
        self.wind_button.clicked.connect(self.button_wind)

        # Battery Button
        self.battery_button = QPushButton()
        self.battery_button.setFixedWidth(120)
        battery_icon  = QPixmap('batticon.png')
        self.battery_button.setIcon(QIcon(battery_icon))
        self.battery_button.setIconSize(QSize(200,40))
        self.battery_button.setStyleSheet("background-color: white")
        self.battery_button.setCheckable(True)
        self.battery_button.clicked.connect(self.button_battery)

        # Generator Button
        self.gen_button = QPushButton()
        self.gen_button.setFixedWidth(120)
        gen_icon  = QPixmap('dieselicon.png')
        self.gen_button.setIcon(QIcon(gen_icon))
        self.gen_button.setIconSize(QSize(200,40))
        self.gen_button.setStyleSheet("background-color: white")
        self.gen_button.setCheckable(True)
        self.gen_button.clicked.connect(self.button_gen)

        # Calendar Code
        cal = QCalendarWidget(self)
        end_cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        end_cal.setGridVisible(True)
        end_cal.setFixedWidth(300)
        cal.setFixedWidth(300)

        cal.clicked[QtCore.QDate].connect(self.showDate)
        end_cal.clicked[QtCore.QDate].connect(self.show2Date)
        
        self.date = cal.selectedDate()
        cal.setMaximumDate(self.date)
        self.date_end = end_cal.selectedDate()
        end_cal.setMaximumDate(self.date_end)
        globals.start_date = self.date.toString('yyyyMMdd')
        globals.end_date = self.date_end.toString('yyyyMMdd')
        self.duration = self.date.daysTo(self.date_end)
        globals.duration = self.duration
        print(self.duration)

        calabel = QLabel('Project Duration')
        calabel.setStyleSheet('color: orange')
        calabel.setFont(labelFont)
        stlabel = QLabel('Select the Start Date Below : ')
        stlabel.setStyleSheet('color: beige')
        endlabel = QLabel('Select the End Date Below : ')
        endlabel.setStyleSheet('color: beige')

        vline = QFrame()
        vline.setFrameStyle(QFrame.VLine | QFrame.Sunken)

        layout = QGridLayout()
        layout.addWidget(title1, 0, 0, 1, 2)
        layout.addWidget(label1, 1, 0, 1, 2)
        layout.addWidget(self.edit_title, 1, 1, 1, 5)
        layout.addWidget(label2, 2, 0, 1, 2)
        layout.addWidget(self.edit_desc, 2, 1, 1, 5)
        layout.addWidget(label3, 8, 7, 1, 4)
        layout.addWidget(space, 0, 6)
        layout.addWidget(maptitle, 1, 6)
        layout.addWidget(self._map_widget, 2, 6, 6, 6)
        layout.addWidget(locAddr, 5, 0, 1, 5)
        layout.addWidget(search_button, 6, 3, 1, 2)
        layout.addWidget(self.text_name, 6, 0, 1,7)
        layout.addWidget(self.solar_button, 9, 7, 2, 2)
        layout.addWidget(self.wind_button, 9, 9, 2, 2)
        layout.addWidget(self.battery_button, 11, 7, 2, 2)
        layout.addWidget(self.gen_button, 11, 9, 2, 2)
        layout.addWidget(cal, 9, 0, 8, 2)
        layout.addWidget(end_cal, 9, 2, 8, 4)
        layout.addWidget(calabel, 7, 0, 1, 4)
        layout.addWidget(stlabel, 8, 0, 1, 5)
        layout.addWidget(endlabel, 8, 2, 1,5)
        layout.addWidget(self.image, 0, 11, 1, 4)
        self.setLayout(layout)
        self.refresh_data() 
        self.search()
        

    @QtCore.pyqtSlot()
    def search(self):
        y = str(self.text_name.text())
        ctx = ssl.create_default_context(cafile=certifi.where())
        geopy.geocoders.options.default_ssl_context = ctx
        geopy.geocoders.options.default_user_agent = "my-application"

        nom = Nominatim(timeout=10)
        n = nom.geocode(y)
        globals.latitude = n.latitude
        globals.longitude = n.longitude
        globals.address = y
        print(n.latitude, n.longitude)
        print(y)
        self.lat_value = globals.latitude
        self.lon_value = globals.longitude
        lat = self.lat_value
        lng = self.lon_value
        self._map_widget.moveMarker(QtPositioning.QGeoCoordinate(lat, lng))
        print(globals.latitude, globals.longitude)
        self.update_data()
        print(globals.sys_data['sys_config'])
        
    @QtCore.pyqtSlot(bool)
    def button_solar(self,checked):
        if checked:
            print("Solar Button Clicked")
            globals.sys_data['is_pv'] = True
            print(globals.sys_data['is_pv'])
            self.rowOverride = True
        elif not checked:
            self.rowOverride = False

    @QtCore.pyqtSlot(bool)
    def button_wind(self,checked):
        if checked:
            print("Wind Button Clicked")
            globals.sys_data['is_wind'] = True
            self.rowOverride = True
        elif not checked:
            self.rowOverride = False

    @QtCore.pyqtSlot(bool)
    def button_battery(self,checked):
        if checked:
            print("Battery Button Clicked")
            globals.sys_data['is_batt'] = True
            self.rowOverride = True
        elif not checked:
            self.rowOverride = False

    @QtCore.pyqtSlot(bool)
    def button_gen(self,checked):
        if checked:
            print("Generator Button Clicked")
            globals.sys_data['is_gen'] = True
            self.rowOverride = True
        elif not checked:
            self.rowOverride = False

    # Method Updates the Global Variables
    def update_data(self):
        globals.sys_data['proj_title'] = self.edit_title.text()
        globals.sys_data['proj_desc'] = self.edit_desc.toPlainText()
        globals.sys_data['sys_config'] = self.combo_config.currentIndex()

    # Updates the selected start date globally
    def showDate(self, date):
        self.start_date = date.toString('yyyyMMdd')
        self.date = date
        globals.start_date = self.start_date
        print(self.start_date)

    # Updates the selected end date globally
    def show2Date(self, date_end):
        self.end_date = date_end.toString('yyyyMMdd')
        self.date_end = date_end
        globals.end_date = self.end_date
        self.duration = self.date.daysTo(self.date_end)
        globals.duration = self.duration
        print(self.end_date)
        print(globals.duration)

    # Refreshes the Data Input Fields with Global Variables
    def refresh_data(self):
        self.edit_title.setText(str(globals.sys_data['proj_title']))
        self.edit_desc.setText(str(globals.sys_data['proj_desc']))
        self.combo_config.setCurrentIndex(globals.sys_data['sys_config'])
        