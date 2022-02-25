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
from dronekit import connect

location = "/dev/ttyACM0"
bitrate = 115200 * 1
vehicle = None

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
camera_width = 550
camera_height = int((camera_width/4)*3)
camera_location_x = int((map_location_x-camera_width))
camera_location_y = int(50)
camera_width_resolution = int(camera_width+55)
camera_height_resolution = int(camera_height)



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret: self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class Window(QWidget):

    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("Python ")
        # setting geometry
        self.setGeometry(50, 50, window_width, window_height)
        # calling methods
        self.UiLivePannel()
        self.UiControlPannel()
        self.UiInformationPannel()
        self.UiDisplayTime()

        # self.timer = QTimer(self)
        # self.timer.setSingleShot(False)
        # self.timer.setInterval(1000)  # in milliseconds, so 5000 = 5 seconds
        # self.timer.timeout.connect(self.UiDisplayTime) # her saniye bitişinde gidipp çağırır
        # self.timer.start()
        # camerada da sürekli bir güncelleme var. bunu engelliyor olabilir
        # başka bir yolda en alttaki ana döngüyü while içine alıp
        # biz kapatana kadar çalışmasını sağlamak.
        # ancak işlemciye fazla yüklenip donup kalıyor. sonrasında fazla döndürmeye çalışıp kapanıyor.
        # çözüm olarak time.sleep(0.100) 100 ms bekleme denedim ancak bunda da kaldırmadı...
        # şuan için iki çözüm yolu var ya telemetriden veri geldiğinde biz güncelleme yapıcağız yada
        # asenkron bir fonksiyon ile sürekli olarak saniye başına güncellicek.
        # eğer gelen veriye göre yaparsak kamera verilerini de etkilememiş olur sadece veri çıktılarını güncelleriz.

    # method for widgets
    def UiDisplayTime(self):
        # SİSTEM SAATİ GÖSTERGESİ
        textlabel = QLabel(self)
        time = QTime.currentTime()
        sistem_saati = time.toString('hh:mm:ss')
        textlabel.setText("Sistem Saati:" + sistem_saati)
        myFont = QtGui.QFont('Arial', 22)
        myFont.setBold(True)
        textlabel.setFont(myFont)
        textlabel.setGeometry(int(window_width - 300), 10, int(window_width / 2), 35)

    def UiInformationPannel(self):

        #UÇUŞ MODU GÖSTERGESİ
        textlabel = QLabel(self)
        ucus_modu = 1234
        textlabel.setText("Aracın Uçuş Modu:"+str(ucus_modu))
        myFont = QtGui.QFont('Arial', 22)
        myFont.setBold(True)
        textlabel.setFont(myFont)
        textlabel.setGeometry(14,10,int(window_width/2),35)

        #information pannel(bilgi paneli)
        textlabel2 = QLabel(self)
        yer_hiz_degeri = 1234
        textlabel2.setText("Aracın Yer Hızı Degeri: "+str(yer_hiz_degeri))
        myFont2 = QtGui.QFont('Arial', 11)
        textlabel2.setFont(myFont2)
        textlabel2.setGeometry(camera_location_x,camera_height+camera_location_y+20,250,22)

        textlabel3 = QLabel(self)
        hava_hiz_degeri = 1234
        textlabel3.setText("Aracın Hava Hızı Degeri: "+str(hava_hiz_degeri))
        textlabel3.setFont(myFont2)
        textlabel3.setGeometry(camera_location_x,camera_height+camera_location_y+45,250,22)

        textlabel4 = QLabel(self)
        textlabel5 = QLabel(self)
        textlabel4.setText("Aracın Enlemi: " + str(coordinate_x))
        textlabel5.setText("Aracın Boylamı: " + str(coordinate_y))
        textlabel4.setFont(myFont2)
        textlabel5.setFont(myFont2)
        textlabel4.setGeometry(camera_location_x, camera_height + camera_location_y + 70, 250, 22)
        textlabel5.setGeometry(camera_location_x, camera_height + camera_location_y + 95, 250, 22)

        textlabel6 = QLabel(self)
        irtifa_degeri = 1234
        textlabel6.setText("Aracın İrtifası: " + str(irtifa_degeri))
        textlabel6.setFont(myFont2)
        textlabel6.setGeometry(camera_location_x, camera_height + camera_location_y + 120, 250, 22)

        textlabel7 = QLabel(self)
        irtifa_degeri = 12
        textlabel7.setText("Aracın pil durumu: %" + str(irtifa_degeri))
        textlabel7.setFont(myFont2)
        textlabel7.setGeometry(camera_location_x+250, camera_height + camera_location_y + 20, 250, 22)

        textlabel8 = QLabel(self)
        telemetri_durumu = 12
        textlabel8.setText("telemetri durumu: " + str(telemetri_durumu))
        textlabel8.setFont(myFont2)
        textlabel8.setGeometry(camera_location_x + 250, camera_height + camera_location_y + 45, 250, 22)

        textlabel8 = QLabel(self)
        ucus_suresi = 12
        textlabel8.setText("Uçuş süresi: " + str(ucus_suresi))
        textlabel8.setFont(myFont2)
        textlabel8.setGeometry(camera_location_x + 250, camera_height + camera_location_y + 70, 250, 22)

        textlabel9 = QLabel(self)
        textlabel9.setText("bağlanma:")
        textlabel9.setFont(myFont2)
        textlabel9.setGeometry(camera_location_x + 250, camera_height + camera_location_y + 95, 80, 22)



    def UiControlPannel(self):

        myFont2 = QtGui.QFont('Arial', 11)
        control_pannel_button_x = int(window_width - 75)
        control_pannel_textbox_x = int(window_width - 187)
        control_pannel_text_x = int(window_width - 335)
        # -------Control Panel Elements--------#
        # koordinat gönder
        label1 = QLabel(self)
        label1.setText("Koordinat gönder")
        label1.setGeometry(control_pannel_text_x, map_height + 10+ map_location_y, 100, 20)
        textbox1 = QLineEdit(self)
        textbox1.setGeometry(control_pannel_textbox_x, map_height + 10+ map_location_y, 100, 20)
        coordinate_button = QPushButton("Gönder", self)
        coordinate_button.setGeometry(control_pannel_button_x, map_height + 10+ map_location_y, 65, 20)  # butonlar arası 5px boşluk
        # araç hızını değiştir
        label2 = QLabel(self)
        label2.setText("Hızı değiştir")
        label2.setGeometry(control_pannel_text_x, map_height + 35+ map_location_y, 100, 20)
        textbox2 = QLineEdit(self)
        textbox2.setGeometry(control_pannel_textbox_x, map_height + 35+ map_location_y, 100, 20)
        hiz_button = QPushButton("Gönder", self)
        hiz_button.setGeometry(control_pannel_button_x, map_height + 35+ map_location_y, 65, 20)  # butonlar arası 5px boşluk
        # araç irtifasını değiştir
        label3 = QLabel(self)
        label3.setText("İrtifa değiştir")
        label3.setGeometry(control_pannel_text_x, map_height + 60+ map_location_y, 100, 20)
        textbox3 = QLineEdit(self)
        textbox3.setGeometry(control_pannel_textbox_x, map_height + 60+ map_location_y, 100, 20)
        irtifa_button = QPushButton("Gönder", self)
        irtifa_button.setGeometry(control_pannel_button_x, map_height + 60+ map_location_y, 65, 20)  # butonlar arası 5px boşluk
        # uçuş modu seçimi
        label3 = QLabel(self)
        label3.setText("Uçuş modunu değiştir")
        label3.setGeometry(control_pannel_text_x, map_height + 85+ map_location_y, 200, 20)
        onayla_button = QPushButton("Onayla", self)
        onayla_button.setGeometry(control_pannel_button_x, map_height + 85+ map_location_y, 65, 20)  # butonlar arası 5px boşluk
        # uçuş modları
        radio1 = QRadioButton("Otonom Kalkis", self)
        radio1.setGeometry(control_pannel_text_x+50, map_height + 110+ map_location_y, 150, 20)

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

        textlabel10 = QLabel(self)
        ucus_suresi = 12
        textlabel10.setText("bitrate:")
        textlabel10.setFont(myFont2)
        textlabel10.setGeometry(camera_location_x + 250, camera_height + camera_location_y + 120, 80, 22)

        textbox5 = QLineEdit(self)
        textbox5.setText("/dev/ttyACM0")
        textbox5.setGeometry(camera_location_x + 330, camera_height + camera_location_y + 95, 95, 20)
        baglan_button = QPushButton("bağlan", self)
        baglan_button.setGeometry(camera_location_x + 440, camera_height + camera_location_y + 95, 65,20)  # butonlar arası 5px boşluk


        textbox6 = QLineEdit(self)
        textbox6.setText("115200")
        textbox6.setGeometry(camera_location_x + 330, camera_height + camera_location_y + 120, 95, 20)
        baglan2_button = QPushButton("kes", self)
        baglan2_button.setGeometry(camera_location_x + 440, camera_height + camera_location_y + 120, 65,20)  # butonlar arası 5px boşluk

        def baglan():
            location = textbox5.text()
            print("location: " + location)
            bitrate = textbox6.text() * 1
            print("bitrate: " + bitrate)
            vehicle = connect(location, wait_ready=True, baud=bitrate)
            print("Mode: %s" % vehicle.mode.name)

        def baglan2():
            print("hi")
        # adding action to a button
        coordinate_button.clicked.connect(self.koordinat_gonder)
        hiz_button.clicked.connect(self.hiz_gonder)
        irtifa_button.clicked.connect(self.irtifa_gonder)
        onayla_button.clicked.connect(self.ucus_modunu_gonder)
        baglan_button.clicked.connect(baglan)
        baglan2_button.clicked.connect(baglan2)

    def UiLivePannel(self):
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
        self.image_label.setGeometry(camera_location_x,camera_location_y,camera_width, camera_height)
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
        p = convert_to_Qt_format.scaled(camera_width_resolution,camera_height_resolution, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    #Button events ...
    def koordinat_gonder(self):
        BR = QMessageBox.question(self, 'Mission Planner Message',"koordinati değiştir ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if BR == QMessageBox.Yes:
            print('Yes clicked.')
        else:
            print('No clicked.')


    def hiz_gonder(self):
        BR = QMessageBox.question(self, 'Mission Planner Message', "hızı değiştir ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if BR == QMessageBox.Yes:
            print('Yes clicked.')
        else:
            print('No clicked.')

    def irtifa_gonder(self):
        BR = QMessageBox.question(self, 'Mission Planner Message', "irtifayı değiştir ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if BR == QMessageBox.Yes:
            print('Yes clicked.')
        else:
            print('No clicked.')

    def ucus_modunu_gonder(self):
        BR = QMessageBox.question(self, 'Mission Planner Message', "Uçuş modunu değiştir ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if BR == QMessageBox.Yes:
            print('Yes clicked.')
        else:
            print('No clicked.')



if __name__=="__main__":
    # create pyqt5 app
    App = QApplication(sys.argv)
    # create the instance of our Window
    window = Window()
    window.show()
    # start the app
    sys.exit(App.exec())
