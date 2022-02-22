# importing libraries
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys,os
import cv2
import numpy as np
import io
import folium


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

#coordinates
coordinate_x = 41.005858 #enlem
coordinate_y = 29.009490 #boylam

#window
window_width = 1120
window_height = 630

#map
map_width = 375
map_height = 375
map_location_x = int(window_width-map_width)
map_location_y = int(10)

#camera
camera_widht = 375
camera_height = 375
camera_location_x = int(map_location_x-camera_widht-int(camera_widht/20))
camera_location_y = int(10)
camera_widht_resolution = int(camera_widht+50)
camera_height_resolution = int(camera_height)

#buttons size
#webView.setContentsMargins(2,2,2,2)#default button margin



class Window(QWidget):

    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("Python ")
        # setting geometry
        self.setGeometry(100, 100, window_width, window_height)
        # calling methods
        self.UiComponents()

    # method for widgets

    def UiComponents(self):
        # -------Map Elements--------#
        webView = QWebEngineView(self)
        webView.setGeometry(map_location_x, map_location_y, map_width, map_height)
        webView.setContentsMargins(10,10,10,10)
        # coordinate = (37.8199286, -122.4782551) # usa da bir yer
        coordinate = (coordinate_x, coordinate_y)
        m = folium.Map(
            tiles='Stamen Terrain', zoom_start=13, location=coordinate
        )
        # save map
        data = io.BytesIO()
        m.save(data, close_file=False)
        webView.setHtml(data.getvalue().decode())
        # -------Map Elements--------#

        #-------Video Elements--------#
        self.image_label = QLabel(self)
        self.image_label.setGeometry(camera_location_x,camera_location_y,camera_widht, camera_height)
        self.image_label.setContentsMargins(10, 10, 10, 10)
        #gui üzerindeki boyut ve konum belirler
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        # -------Video Elements--------#

        # -------Control Panel Elements--------#
        #koordinat gönder
        label1 = QLabel(self)
        label1.setText("Koordinat gönder")
        label1.setGeometry(window_width-295, map_height+20, 100, 20)
        textbox1 = QLineEdit(self)
        textbox1.setGeometry(window_width-187,map_height+20,100,20)
        button1 = QPushButton("Gönder", self)
        button1.setGeometry(window_width-75, map_height+20, 65, 20)#butonlar arası 5px boşluk
        #araç hızını değiştir
        label2 = QLabel(self)
        label2.setText("Hızı değiştir")
        label2.setGeometry(window_width - 295, map_height + 45, 100, 20)
        textbox2 = QLineEdit(self)
        textbox2.setGeometry(window_width - 187, map_height + 45, 100, 20)
        button2 = QPushButton("Gönder", self)
        button2.setGeometry(window_width - 75, map_height + 45, 65, 20)  # butonlar arası 5px boşluk
        #araç irtifasını değiştir
        label3 = QLabel(self)
        label3.setText("İrtifa değiştir")
        label3.setGeometry(window_width - 295, map_height + 70, 100, 20)
        textbox3 = QLineEdit(self)
        textbox3.setGeometry(window_width - 187, map_height + 70, 100, 20)
        button3 = QPushButton("Gönder", self)
        button3.setGeometry(window_width - 75, map_height + 70, 65, 20)  # butonlar arası 5px boşluk
        #uçuş modu seçimi
        label3 = QLabel(self)
        label3.setText("Uçuş modunu değiştir")
        label3.setGeometry(window_width - 295, map_height + 95, 200, 20)
        button3 = QPushButton("Onayla", self)
        button3.setGeometry(window_width - 75, map_height + 95, 65, 20)  # butonlar arası 5px boşluk
        #uçuş modları
        radio1 = QRadioButton("Otonom Kalkis",self)
        radio1.setGeometry(window_width - 245, map_height + 120, 150, 20)

        radio2 = QRadioButton("Otonom İniş", self)
        radio2.setGeometry(window_width - 245, map_height + 145, 150, 20)

        radio3 = QRadioButton("Otonom Uçuş", self)
        radio3.setGeometry(window_width - 245, map_height + 170, 150, 20)

        radio4 = QRadioButton("Bul ve Takip Et", self)
        radio4.setGeometry(window_width - 245, map_height + 195, 150, 20)

        radio5 = QRadioButton("Kamikaze", self)
        radio5.setGeometry(window_width - 245, map_height + 220, 150, 20)
        # -------Control Panel Elements--------#



    def clickme(self):
        # printing pressed
        print("pressed")

    def closeEvent(self, event):
        self.thread.stop()
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
        p = convert_to_Qt_format.scaled(camera_widht_resolution,camera_height_resolution, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
if __name__=="__main__":
    # create pyqt5 app
    App = QApplication(sys.argv)
    # create the instance of our Window
    window = Window()
    window.show()
    # start the app
    sys.exit(App.exec())