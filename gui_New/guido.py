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
window_width = 945
window_height = 630

#map
map_width = 355
map_height = 355
map_location_x = int(window_width-map_width)
map_location_y = int(40)

#camera
camera_widht = 550
camera_height = int((camera_widht/4)*3)
camera_location_x = int((map_location_x-camera_widht))
camera_location_y = int(50)
camera_widht_resolution = int(camera_widht+55)
camera_height_resolution = int(camera_height)




class Window(QWidget):

    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("Python ")
        # setting geometry
        self.setGeometry(50, 50, window_width, window_height)
        # calling methods
        self.UiComponents()
        self.UiControlPannel()
        self.UiInformationPannel()

    # method for widgets
    def UiInformationPannel(self):
        #UÇUŞ MODU GÖSTERGESİ
        textlabel = QLabel(self)
        textlabel.setText("Aracın Uçuş Modu:OTONOM")
        myFont = QtGui.QFont('Arial', 22)
        myFont.setBold(True)
        textlabel.setFont(myFont)
        textlabel.setGeometry(14,10,int(window_width/2),35)
        #information pannel(bilgi paneli)
        textlabel = QLabel(self)
        textlabel.setText("Aracın Uçuş Modu:OTONOM")
        textlabel.setFont(myFont)
        textlabel.setGeometry(14, 10, int(window_width / 2), 35)
    def UiControlPannel(self):

        control_pannel_button_x = int(window_width - 75)
        control_pannel_textbox_x = int(window_width - 187)
        control_pannel_text_x = int(window_width - 295)
        # -------Control Panel Elements--------#
        # koordinat gönder
        label1 = QLabel(self)
        label1.setText("Koordinat gönder")
        label1.setGeometry(control_pannel_text_x, map_height + 10+ map_location_y, 100, 20)
        textbox1 = QLineEdit(self)
        textbox1.setGeometry(control_pannel_textbox_x, map_height + 10+ map_location_y, 100, 20)
        button1 = QPushButton("Gönder", self)
        button1.setGeometry(control_pannel_button_x, map_height + 10+ map_location_y, 65, 20)  # butonlar arası 5px boşluk
        # araç hızını değiştir
        label2 = QLabel(self)
        label2.setText("Hızı değiştir")
        label2.setGeometry(control_pannel_text_x, map_height + 35+ map_location_y, 100, 20)
        textbox2 = QLineEdit(self)
        textbox2.setGeometry(control_pannel_textbox_x, map_height + 35+ map_location_y, 100, 20)
        button2 = QPushButton("Gönder", self)
        button2.setGeometry(control_pannel_button_x, map_height + 35+ map_location_y, 65, 20)  # butonlar arası 5px boşluk
        # araç irtifasını değiştir
        label3 = QLabel(self)
        label3.setText("İrtifa değiştir")
        label3.setGeometry(control_pannel_text_x, map_height + 60+ map_location_y, 100, 20)
        textbox3 = QLineEdit(self)
        textbox3.setGeometry(control_pannel_textbox_x, map_height + 60+ map_location_y, 100, 20)
        button3 = QPushButton("Gönder", self)
        button3.setGeometry(control_pannel_button_x, map_height + 60+ map_location_y, 65, 20)  # butonlar arası 5px boşluk
        # uçuş modu seçimi
        label3 = QLabel(self)
        label3.setText("Uçuş modunu değiştir")
        label3.setGeometry(control_pannel_text_x, map_height + 85+ map_location_y, 200, 20)
        button3 = QPushButton("Onayla", self)
        button3.setGeometry(control_pannel_button_x, map_height + 85+ map_location_y, 65, 20)  # butonlar arası 5px boşluk
        # uçuş modları
        radio1 = QRadioButton("Otonom Kalkis", self)
        radio1.setGeometry(window_width - 245, map_height + 110+ map_location_y, 150, 20)

        radio2 = QRadioButton("Otonom İniş", self)
        radio2.setGeometry(control_pannel_text_x+50, map_height + 135+ map_location_y, 150, 20)

        radio4 = QRadioButton("Bul ve Takip Et", self)
        radio4.setGeometry(control_pannel_text_x+50, map_height + 160+ map_location_y, 150, 20)

        radio5 = QRadioButton("Kamikaze", self)
        radio5.setGeometry(control_pannel_text_x+50, map_height + 185+ map_location_y, 150, 20)

        textbox4 = QLineEdit(self)
        textbox4.setGeometry(control_pannel_text_x+50, map_height + 210+ map_location_y, 100, 20)
        textbox4 = QLineEdit(self)
        textbox4.setGeometry(control_pannel_text_x+155, map_height + 210+ map_location_y, 100, 20)
        # -------Control Panel Elements--------#
    def UiComponents(self):
        # -------Map Elements--------#
        webView = QWebEngineView(self)
        webView.setGeometry(map_location_x, map_location_y, map_width, map_height)
        webView.setContentsMargins(10,10,10,10)
        # coordinate = (37.8199286, -122.4782551) # usa da bir yer
        coordinate = (coordinate_x, coordinate_y)
        m = folium.Map(
            tiles='Stamen Terrain', zoom_start=10, location=coordinate
        )
        # save map
        data = io.BytesIO()
        m.save(data, close_file=False)
        webView.setHtml(data.getvalue().decode())
        # -------Map Elements--------#

        #-------Video Elements--------#
        self.image_label = QLabel(self)
        self.image_label.setGeometry(camera_location_x,camera_location_y,camera_widht, camera_height)
        #gui üzerindeki boyut ve konum belirler
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        # -------Video Elements--------#

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