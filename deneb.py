from branca.element import Element
from dronekit import connect, VehicleMode
import dronekit
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import uic
import cv2, sys, os, serial,json
import numpy as np
import io, folium, time, SerialCom
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from folium.plugins import Draw
from PyQt5 import QtWidgets, QtWebEngineWidgets

arr = []


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        print(msg)  # Check js errors
        if 'coordinates' in msg:
            self.parent.handleConsoleMessage(msg)


coordinate_lat = 41.005858
coordinate_lon = 29.009490


# >>>>>>>>>>>>>>>>>>>>ROTA PLANNER WINDOW CLASS<<<<<<<<<<<<<<<<<<<<#
class MapCommand(QDialog):
    """map coordinate dialog pannel"""

    def __init__(self, parent=None):
        background_color = "background-color:#0F0E0E"
        button_background_color = "background-color:#541212"
        text_color = "color:#8B9A46"
        border_color = "#EEEEEE"
        super().__init__(parent)
        uic.loadUi("dialog.ui", self)
        self.UiMap()
        self.resize(550, 550)
        self.setStyleSheet(background_color)
        self.pushButton.setStyleSheet("QPushButton {" + button_background_color + ";" + text_color + ";}")

    def UiMap(self):
        web = QtWebEngineWidgets.QWebEngineView(self)
        web.setGeometry(30, 10, 500, 500)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        cor = (41.005858, 29.009490)
        m = folium.Map(location=cor, tiles="Stamen Terrain", zoom_start=13, )
        # icon = folium.features.CustomIcon("video-photo/para.jpg", icon_size=(30, 30))  # Creating a custom Icon
        # folium.Marker(location=cor, icon=icon).add_to(m)
        m = self.add_customjs(m)

        draw = Draw(
            draw_options={
                'polyline': {'allowIntersection': True},

                'rectangle': False,
                'polygon': False,
                'circle': False,
                'marker': True,
                'circlemarker': False,
            },
            edit_options={'edit': False})
        m.add_child(draw)

        data = io.BytesIO()
        m.save(data, close_file=False)
        #self.setGeometry(100, 100, 600, 600)  # screen x,screen y ,pencere x,pencere y
        page = WebEnginePage(self)
        web.setPage(page)
        web.setHtml(data.getvalue().decode())
        self.setWindowTitle("chart")
        layout.addWidget(web)

    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                    function(e){{
                        var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                        console.log(data)}});"""
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        # Insert new element or custom JS
        html.script._children[e.get_name()] = e
        return map_object

    def handleConsoleMessage(self, msg):
        data = json.loads(msg)
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']
        coords = f"latitude: {lat} longitude: {lng}"
        # self.label.setText(coords)
        print("copied cordinates: " + coords)  # cordinatlar oldugu gibi burda coords.
        arr.append([coords])


# >>>>>>>>>>>>>>>>>>>>ROTA PLANNER WINDOW CLASS<<<<<<<<<<<<<<<<<<<<#

# >>>>>>>>>>>>>>>>>>>>VIDEO AND INFO THREAD<<<<<<<<<<<<<<<<<<<<#
class IhaThread(QThread):
    any_signal = pyqtSignal(int)
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, parent=None, index=0):
        super(IhaThread, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        if self.index == 255:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            while self.is_running:
                ret, cv_img = cap.read()
                if ret: self.change_pixmap_signal.emit(cv_img)
            cap.release()

        if self.index != 255:
            cnt = 0
            if self.index == 1:
                while self.is_running:
                    cnt = cnt + 1
                    self.any_signal.emit(cnt)
                    if cnt == 1499: cnt = 0
                    time.sleep(0.01)
            if self.index == 2:
                while self.is_running:
                    cnt = cnt + 1
                    self.any_signal.emit(cnt)
                    if cnt == 99: cnt = 0
                    time.sleep(1)
        # while self.is_running:
        # if self.index == 1  :self.any_signal.emit(vehicle.groundspeed)
        # if self.index == 2  :self.any_signal.emit(vehicle.airspeed)
        # if self.index == 3 :self.any_signal.emit()
        # if self.index == 4 :self.any_signal.emit(vehicle.velocity)
        # if self.index == 5 :self.any_signal.emit()
        # if self.index == 6 :self.any_signal.emit()
        # if self.index == 7  :self.any_signal.emit(vehicle.location.global_frame.alt)
        # if self.index == 8  :self.any_signal.emit(vehicle.heading)
        # if self.index == 9  :self.any_signal.emit(vehicle.mode.name)

        # if self.index == 10  :self.any_signal.emit(vehicle.battery.voltage)
        ##if self.index == #  :self.any_signal.emit(vehicle.last_heartbeat)
        ##if self.index == #  :self.any_signal.emit(vehicle.rangefinder.distance)
        ##if self.index == #  :self.any_signal.emit(vehicle.rangefinder.voltage)
        # time.sleep(0.5)

    def stop(self):
        self.is_running = False
        if self.index == 255:
            self.wait()
        if self.index != 255:
            self.terminate()


# >>>>>>>>>>>>>>>>>>>>VIDEO AND INFO THREAD<<<<<<<<<<<<<<<<<<<<#

class Deneb(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("deneme.ui", self)
        self.connection_status = 0
        self.setWindowIcon(QtGui.QIcon('assets/iha.png'))
        self.connect_button.clicked.connect(self.start_work)
        self.rota_plan_planla_button.clicked.connect(self.mapdialog)
        self.thread = {}
        self.val = {}
        self.temp = {}

    # >>>>>>>>>>>>>>>>>>>>SISTEM SAATI<<<<<<<<<<<<<<<<<<<<#
    def UiClock(self):
        self.screenTimer = QTimer()
        self.screenTimer.setInterval(1000)
        self.screenTimer.timeout.connect(self.showTime)
        self.screenTimer.start()

    def showTime(self):

        current_time = QTime.currentTime()
        time = current_time.toString('hh:mm:ss')
        self.sistem_saati_label.setText("Sistem saati " + time)
        self.val = SerialCom.CheckAvailableSerial()
        if self.val != self.temp:
            self.port_combo_box.clear()
            for x in self.val:
                self.temp = self.val
                self.port_combo_box.addItem(self.val[x])

    # >>>>>>>>>>>>>>>>>>>>SISTEM SAATI<<<<<<<<<<<<<<<<<<<<#

    # >>>>>>>>>>>>>>>>>>>>ROTA PLANNER WINDOW<<<<<<<<<<<<<<<<<<<<#
    def mapdialog(self):
        dlg = MapCommand(self)
        dlg.exec()

    # >>>>>>>>>>>>>>>>>>>>ROTA PLANNER WINDOW<<<<<<<<<<<<<<<<<<<<#

    # >>>>>>>>>>>>>>>>>>>>CONNECTION BUTTON SLOT<<<<<<<<<<<<<<<<<<<<#
    def start_work(self):
        if self.connection_status == 0:
            self.connection_status = 1
            self.connect_button.setStyleSheet(
                "QPushButton::enabled{image : url(assets/disconnect.png)}QPushButton::pressed{image : url(assets/disconnect_press.png)}")
            self.vehicle = self.connect_vehicle()
            self.thread[255] = IhaThread(parent=None, index=255)
            self.thread[255].change_pixmap_signal.connect(self.update_image)
            self.thread[255].start()
            self.thread[1] = IhaThread(parent=None, index=1)
            self.thread[1].any_signal.connect(self.ground_speed)  # burada da sinyal bağlanmış
            self.thread[1].start()
            self.thread[2] = IhaThread(parent=None, index=2)
            self.thread[2].any_signal.connect(self.air_speed)
            self.thread[2].start()
            self.thread[3] = IhaThread(parent=None, index=3)
            self.thread[3].any_signal.connect(self.irtifa)
            self.thread[3].start()
            self.thread[4] = IhaThread(parent=None, index=4)
            self.thread[4].any_signal.connect(self.surat)
            self.thread[4].start()
            self.thread[5] = IhaThread(parent=None, index=5)
            self.thread[5].any_signal.connect(self.latitude)
            self.thread[5].start()
            self.thread[6] = IhaThread(parent=None, index=6)
            self.thread[6].any_signal.connect(self.longitude)
            self.thread[6].start()
            self.thread[7] = IhaThread(parent=None, index=7)
            self.thread[7].any_signal.connect(self.altitude)
            self.thread[7].start()
            self.thread[8] = IhaThread(parent=None, index=8)
            self.thread[8].any_signal.connect(self.yaw)
            self.thread[8].start()
            self.thread[9] = IhaThread(parent=None, index=9)
            self.thread[9].any_signal.connect(self.flight_mode)
            self.thread[9].start()
            self.thread[10] = IhaThread(parent=None, index=10)
            self.thread[10].any_signal.connect(self.pil)
            self.thread[10].start()

        elif self.connection_status == 1:
            self.connection_status = 0
            self.connect_button.setStyleSheet(
                "QPushButton::enabled{image : url(assets/connect.png)}QPushButton::pressed{image : url(assets/connect_press.png)}")
            self.thread[255].stop()
            self.thread[1].stop()
            self.thread[2].stop()
            self.thread[3].stop()
            self.thread[4].stop()
            self.thread[5].stop()
            self.thread[6].stop()
            self.thread[7].stop()
            self.thread[8].stop()
            self.thread[9].stop()
            self.thread[10].stop()

    # >>>>>>>>>>>>>>>>>>>>CONNECTION BUTTON SLOT<<<<<<<<<<<<<<<<<<<<#

    # >>>>>>>>>>>>>>>>>>>>THREAD UPDATE SLOT<<<<<<<<<<<<<<<<<<<<#
    def ground_speed(self, counter):
        self.yer_hizi_gauge.updateValue(counter)
        self.yer_hizi_value_label.setText(str(float(counter)))

    def air_speed(self, counter):
        self.hava_hizi_gauge.updateValue(counter)
        self.hava_hizi_value_label.setText(str(float(counter)))

    def irtifa(self, counter):
        self.irtifa_gauge.updateValue(counter)
        self.altitude_value_label.setText(str(float(counter)))

    def surat(self, counter):
        self.surat_gauge.updateValue(counter)

    def latitude(self, counter):
        self.latitude_value_label.setText(str(float(counter)))

    def longitude(self, counter):
        self.longitude_value_label.setText(str(float(counter)))

    def altitude(self, counter):
        self.altitude_value_label.setText(str(float(counter)))

    def yaw(self, counter):
        self.yaw_value_label.setText(str(float(counter)))

    def flight_mode(self, counter):
        self.ucus_modu_label.setText(str(float(counter)))

    def pil(self, counter):
        self.pil_voltaji_label.setText(str(float(counter)))

    # >>>>>>>>>>>>>>>>>>>>THREAD UPDATE SLOT<<<<<<<<<<<<<<<<<<<<#

    # >>>>>>>>>>>>>>>>>>>>VEHICLE CONNECTION<<<<<<<<<<<<<<<<<<<<#
    def connect_vehicle(self):
        # return SerialCom.connectSerialDevice(COM14,115200)
        pass

    # >>>>>>>>>>>>>>>>>>>>VEHICLE CONNECTION<<<<<<<<<<<<<<<<<<<<#

    # >>>>>>>>>>>>>>>>>>>>MAP<<<<<<<<<<<<<<<<<<<<#
    def UiMap(self):
        self.webView = QWebEngineView()
        self.setLayout(self.layout_map)
        self.layout_map.addWidget(self.webView)
        # coordinate = (37.8199286, -122.4782551) # usa da bir yer
        coordinate = (coordinate_lat, coordinate_lon)
        m = folium.Map(
            tiles='Stamen Terrain', zoom_start=10, location=coordinate
        )
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

    # >>>>>>>>>>>>>>>>>>>>MAP<<<<<<<<<<<<<<<<<<<<#

    # >>>>>>>>>>>>>>>>>>>>VIDEO CAPTURE<<<<<<<<<<<<<<<<<<<<#
    def closeEvent(self, event):
        self.thread[255].stop()
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
        p = convert_to_Qt_format.scaled(700, 800, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    # >>>>>>>>>>>>>>>>>>>>VIDEO CAPTURE<<<<<<<<<<<<<<<<<<<<#

    # >>>>>>>>>>>>>>>>>>>>UI WIDGET SET<<<<<<<<<<<<<<<<<<<<#
    def ui_widget_set(self):

        background_color = "background-color:#0F0E0E"
        button_background_color = "background-color:#541212"
        text_color = "color:#8B9A46"
        border_color = "#EEEEEE"

        self.yer_hizi_gauge.setGaugeTheme(0)
        self.yer_hizi_gauge.units = "m/s"
        self.yer_hizi_gauge.maxValue = 1500
        self.yer_hizi_gauge.scalaCount = 5
        self.yer_hizi_gauge.setEnableBarGraph(False)
        self.yer_hizi_gauge.setNeedleColor(R=255, G=0, B=0)
        self.yer_hizi_gauge.setMouseTracking(False)
        self.hava_hizi_gauge.setGaugeTheme(0)
        self.hava_hizi_gauge.units = "m/s"
        self.hava_hizi_gauge.maxValue = 100
        self.hava_hizi_gauge.scalaCount = 5
        self.hava_hizi_gauge.setEnableBarGraph(False)
        self.hava_hizi_gauge.setNeedleColor(R=255, G=0, B=0)
        self.hava_hizi_gauge.setMouseTracking(False)
        self.irtifa_gauge.setGaugeTheme(0)
        self.irtifa_gauge.units = "m"
        self.irtifa_gauge.maxValue = 1000
        self.irtifa_gauge.scalaCount = 5
        self.irtifa_gauge.setNeedleColor(R=255, G=0, B=0)
        self.irtifa_gauge.setMouseTracking(False)
        self.surat_gauge.setGaugeTheme(0)
        self.surat_gauge.units = "m/s"
        self.surat_gauge.maxValue = 1000
        self.surat_gauge.scalaCount = 5
        self.surat_gauge.setEnableBarGraph(False)
        self.surat_gauge.setNeedleColor(R=255, G=0, B=0)
        self.surat_gauge.setMouseTracking(False)
        self.setWindowTitle("IHA MARMARA-ORION")
        self.main_widget.setStyleSheet(background_color)
        self.ucus_modu_label.setStyleSheet(text_color)
        self.flight_time_label.setStyleSheet(text_color)
        self.pil_text_label.setStyleSheet(text_color)
        self.pil_voltaji_label.setStyleSheet(text_color)
        self.yer_hizi_label.setStyleSheet(text_color)
        self.hava_hizi_label.setStyleSheet(text_color)
        self.irtifa_label.setStyleSheet(text_color)
        self.surat_label.setStyleSheet(text_color)
        self.send_coor_text_label.setStyleSheet(text_color)
        self.send_speed_text_label.setStyleSheet(text_color)
        self.send_alt_text_label.setStyleSheet(text_color)
        self.rota_plan_text_label.setStyleSheet(text_color)
        self.yer_hizi_text_label.setStyleSheet(text_color)
        self.yer_hizi_value_label.setStyleSheet(text_color)
        self.hava_hizi_value_label.setStyleSheet(text_color)
        self.hava_hizi_text_label.setStyleSheet(text_color)
        self.latitude_value_label.setStyleSheet(text_color)
        self.latitude_text_label.setStyleSheet(text_color)
        self.longitude_value_label.setStyleSheet(text_color)
        self.longitude_text_label.setStyleSheet(text_color)
        self.altitude_value_label.setStyleSheet(text_color)
        self.altitude_text_label.setStyleSheet(text_color)
        self.yaw_value_label.setStyleSheet(text_color)
        self.yaw_text_label.setStyleSheet(text_color)
        self.inis_radio.setStyleSheet(text_color)
        self.kalkis_radio.setStyleSheet(text_color)
        self.bul_radio.setStyleSheet(text_color)
        self.other_radio.setStyleSheet(text_color)
        self.ucus_modu_text_label.setStyleSheet(text_color)
        self.print_list.setStyleSheet(text_color)
        self.send_coor_lat_edit.setStyleSheet(text_color)
        self.send_coor_lon_edit.setStyleSheet(text_color)
        self.send_speed_edit.setStyleSheet(text_color)
        self.send_alt_edit.setStyleSheet(text_color)
        self.baud_text_label.setStyleSheet(text_color)
        self.port_text_label.setStyleSheet(text_color)
        self.sistem_saati_label.setStyleSheet(text_color)
        self.tabWidget.setStyleSheet(text_color)
        self.send_coor_lat_edit.setStyleSheet("border: 1px solid " + border_color + ";" + text_color + ";")
        self.send_coor_lon_edit.setStyleSheet("border: 1px solid " + border_color + ";" + text_color + ";")
        self.send_speed_edit.setStyleSheet("border: 1px solid " + border_color + ";" + text_color + ";")
        self.send_alt_edit.setStyleSheet("border: 1px solid " + border_color + ";" + text_color + ";")
        self.print_list.setStyleSheet("border: 1px solid " + border_color + ";" + text_color + ";")
        self.port_combo_box.setStyleSheet("QComboBox {" + button_background_color + ";" + text_color + ";}")
        self.baud_combo_box.setStyleSheet("QComboBox {" + button_background_color + ";" + text_color + ";}")
        self.flight_mode_combo_box.setStyleSheet("QComboBox {" + button_background_color + ";" + text_color + ";}")
        self.send_alt_button.setStyleSheet("QPushButton {" + button_background_color + ";" + text_color + ";}")
        self.send_speed_button.setStyleSheet("QPushButton {" + button_background_color + ";" + text_color + ";}")
        self.send_coor_button.setStyleSheet("QPushButton {" + button_background_color + ";" + text_color + ";}")
        self.pushButton_4.setStyleSheet("QPushButton {" + button_background_color + ";" + text_color + ";}")
        self.rota_plan_planla_button.setStyleSheet("QPushButton {" + button_background_color + ";" + text_color + ";}")
        self.rota_plan_onayla_button.setStyleSheet("QPushButton {" + button_background_color + ";" + text_color + ";}")
        self.rota_plan_temizle_button.setStyleSheet("QPushButton {" + button_background_color + ";" + text_color + ";}")
        self.rota_table.setStyleSheet(
            "QTableWidget::foreground {" + text_color + ";}QTableWidget::background {" + button_background_color + ";}")
        self.rota_table.setStyleSheet("QTableWidget {" + button_background_color + ";}")
        self.connect_button.setStyleSheet(
            "QPushButton::enabled{image : url(assets/connect.png)}QPushButton::pressed{image : url(assets/connect_press.png)}")
        self.widget_2.setStyleSheet("QWidget{border-image:url(assets/orion.png)}")
        self.widget_3.setStyleSheet("QWidget{border-image:url(assets/iha.png)}")


# >>>>>>>>>>>>>>>>>>>>UI WIDGET SET<<<<<<<<<<<<<<<<<<<<#

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = Deneb()
    window.ui_widget_set()
    window.UiMap()
    window.UiClock()
    window.show()
    app.exec()
