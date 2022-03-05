

# importing libraries
from dronekit import connect, VehicleMode
import dronekit
import dronekit_sitl
from PyQt5 import QtGui , QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.uic import loadUi
import sys,os
import cv2
import numpy as np
import io
import folium
import serial
import time
from PyQt5.QtGui import QFont, QFontDatabase


global connection_location
global connection_bitrate
connection_location = "COM3"
connection_bitrate = 57600

coordinate_lat = 41.005858
coordinate_lon = 29.009490

# sitl connection.
# sitl = dronekit_sitl.start_default()
# connection_location = sitl.connection_string()

text_color = "color:#FFEBCD"
background_color = "background-color:#09080C"
button_background_color = "background-color:#FFEBCD"


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret: self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class Deneb(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("deneme.ui",self)
        self.setWindowIcon(QtGui.QIcon('iha.png'))

        #guide bulunan analog göstergelerin setup fonksiyonu
        self.UiGaugeSet()
        #Widgetları ayarlama
        self.UiWidgetSet()
        #guideki bağlan butonu
        self.ConnectButton()
        #guideki güncel sistem saati
        self.UiClock()
        #set backgrounds and colors
        self.SetTheme()
        #map
        self.UiMapPanel()

    def UiClock(self):
        self.screenTimer = QTimer()
        self.screenTimer.setInterval(1000)
        self.screenTimer.timeout.connect(self.showTime)
        self.screenTimer.start()

    def showTime(self):
        current_time = QTime.currentTime()
        time = current_time.toString('hh:mm:ss')
        self.ui_time_label.setText("Sistem saati " + time)

    def ConnectButton(self):
        self.baglan_button.clicked.connect(self.Connect)
        self.kes_button.clicked.connect(self.Disconnect)
        
    def Connect(self):

        self.baglan_button.setEnabled(False)
        print("get baudrate and location")
        print("done1")
        connection_location = self.lineEdit_9.text()
        print("done2")
        connection_bitrate = self.lineEdit_10.text()
        print("done3")
        global vehicle
        vehicle = connect(connection_location , wait_ready = False , baud = connection_bitrate)
        print("done4")
        print("Check connection")
        # if vehicle.wait_ready(True):
        print("Connected")
        self.UiCamPanel()
        self.UiWidgetTimer()
        global con_status
        con_status = 1

    def Disconnect(self):
        print("disconnecting")
        con_status = 0
        self.baglan_button.setEnabled(True)
        print("disconnected")

    def UiWidgetTimer(self):
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.CallReaderWriter)
        self.ui_timer.start(1000)

    def CallReaderWriter(self):
        self.ReadData()

    def ReadData(self):
        if con_status == 1:

            # global coordinate_lat
            # global coordinate_lon
            # coordinate_lat = vehicle.location.global_frame.lat  # enlem
            # coordinate_lon = vehicle.location.global_frame.lon  # boylam
            print("done5")
            hava_hiz_degeri = vehicle.airspeed
            yer_hiz_degeri = vehicle.groundspeed
            ucus_modu = vehicle.mode.name
            pil_seviyesi = vehicle.battery.level
            pil_voltaji = vehicle.battery.voltage
            heading = vehicle.heading
            heartbeat = vehicle.last_heartbeat
            telemetri_menzil = vehicle.rangefinder.distance
            telemetri_volt = vehicle.rangefinder.voltage
            irtifa = vehicle.location.global_frame.alt
            surat_degeri = vehicle.velocity

            self.telemetri_range_label.setText("Telemetri Menzil:" + str(telemetri_menzil))
            self.telemetri_volt_label.setText("Telemetri Volt:"+str(telemetri_volt))
            self.heartbeat_label.setText("Last_heartbeat:"+str(heartbeat))
            self.heading_label.setText(" Rota: " + str(heading))
            self.coordinate_lat_label.setText(" Koordinat_lat:")# + str(coordinate_lat)
            self.coordinate_lon_label.setText(" Koordinat_lon:")# + str(coordinate_lon)
            self.gauge_1.updateValue(yer_hiz_degeri)
            self.gauge_2.updateValue(hava_hiz_degeri)
            self.gauge_3.updateValue(irtifa)
            #self.gauge_4.updateValue(int(surat_degeri))
            #print(surat_degeri)
            #sürat [vx,vy,vz] olarak geliyor
            self.ucus_modu_label.setText("Aracın Uçuş Modu:" + ucus_modu)
            self.pil_seviyesi_pbar.setValue(pil_seviyesi)
            self.pil_voltaji_label.setText(str(pil_voltaji) + "V")

    def UiMapPanel(self):
        #bakılacak !!!
        self.webView = QWebEngineView()
        self.setLayout(self.layout_map)
        self.layout_map.addWidget(self.webView)
        # coordinate = (37.8199286, -122.4782551) # usa da bir yer
        coordinate = (coordinate_lat, coordinate_lon)
        m = folium.Map(
            tiles='Stamen Terrain', zoom_start=10, location=coordinate
        )
        # save map
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

    def UiCamPanel(self):
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        #self.thread2.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        #burdaki değişkenler videonun çözünürlüğünü belirler
        #video elementin içindekiler ise videnun ne kadarının
        #gösterileceğini söyler(guide kapladığı yer)
        p = convert_to_Qt_format.scaled(700,800, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def UiGaugeSet(self):

        #yer hizi
        self.gauge_1.setGaugeTheme(0)
        self.gauge_1.units = "M/s"
        self.gauge_1.maxValue = 100
        self.gauge_1.scalaCount = 5
        self.gauge_1.setEnableBarGraph(False)
        self.gauge_1.setNeedleColor(R=255, G=0, B=0)
        self.gauge_1.setMouseTracking(False)

        #hava hizi
        self.gauge_2.setGaugeTheme(0)
        self.gauge_2.units = "M/s"
        self.gauge_2.maxValue = 100
        self.gauge_2.scalaCount = 5
        self.gauge_2.setEnableBarGraph(False)
        self.gauge_2.setNeedleColor(R=255, G=0, B=0)
        self.gauge_2.setMouseTracking(False)

        #irtifa
        self.gauge_3.setGaugeTheme(0)
        self.gauge_3.units = "M"
        self.gauge_3.maxValue = 1000
        self.gauge_3.scalaCount = 5
        self.gauge_3.setNeedleColor(R=255, G=0, B=0)
        self.gauge_3.setMouseTracking(False)

        # sürat
        self.gauge_4.setGaugeTheme(0)
        self.gauge_4.units = "M/s"
        self.gauge_4.maxValue = 1000
        self.gauge_4.scalaCount = 5
        self.gauge_4.setEnableBarGraph(False)
        self.gauge_4.setNeedleColor(R=255, G=0, B=0)
        self.gauge_4.setMouseTracking(False)

    def UiWidgetSet(self):
        #location gettext = lineEdit_9
        self.lineEdit_9.setText = connection_location
        #bitrate gettext = lineEdit_10
        self.lineEdit_10.setText = connection_bitrate

    def SetTheme(self):

        self.main_widget.setStyleSheet(background_color)

        self.ucus_modu_label.setStyleSheet(text_color)
        self.ui_time_label.setStyleSheet(text_color)
        self.label_7.setStyleSheet(text_color)
        self.pil_voltaji_label.setStyleSheet(text_color)
        self.yer_hizi_label.setStyleSheet(text_color)
        self.yer_hizi_label_3.setStyleSheet(text_color)
        self.yer_hizi_label_2.setStyleSheet(text_color)
        self.yer_hizi_label_4.setStyleSheet(text_color)
        self.coordinate_lat_label.setStyleSheet(text_color)
        self.coordinate_lon_label.setStyleSheet(text_color)
        self.heading_label.setStyleSheet(text_color)
        self.heartbeat_label.setStyleSheet(text_color)
        self.telemetri_range_label.setStyleSheet(text_color)
        self.telemetri_volt_label.setStyleSheet(text_color)
        self.label_4.setStyleSheet(text_color)
        self.label_2.setStyleSheet(text_color)
        self.label_3.setStyleSheet(text_color)
        self.radioButton.setStyleSheet(text_color)
        self.radioButton_2.setStyleSheet(text_color)
        self.radioButton_3.setStyleSheet(text_color)
        self.radioButton_4.setStyleSheet(text_color)
        self.label_8.setStyleSheet(text_color)
        self.label_9.setStyleSheet(text_color)
        self.pil_seviyesi_pbar.setStyleSheet(text_color)
        self.label_6.setStyleSheet(text_color)
        self.listWidget.setStyleSheet(text_color)
        self.lineEdit_2.setStyleSheet(text_color)
        self.lineEdit.setStyleSheet(text_color)
        self.lineEdit_8.setStyleSheet(text_color)
        self.lineEdit_5.setStyleSheet(text_color)
        self.lineEdit_3.setStyleSheet(text_color)
        self.lineEdit_4.setStyleSheet(text_color)
        self.lineEdit_7.setStyleSheet(text_color)
        self.lineEdit_6.setStyleSheet(text_color)
        self.lineEdit_9.setStyleSheet(text_color)
        self.lineEdit_10.setStyleSheet(text_color)

        self.pushButton_2.setStyleSheet(button_background_color)
        self.pushButton.setStyleSheet(button_background_color)
        self.pushButton_3.setStyleSheet(button_background_color)
        self.pushButton_4.setStyleSheet(button_background_color)
        self.pushButton_5.setStyleSheet(button_background_color)

app = QApplication([])
window = Deneb()
window.show()
app.exec_()