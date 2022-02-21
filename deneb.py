# TODO: requirements.txt
from PyQt5 import QtGui # pip install PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, os
import cv2
import numpy as np # pip install numpy
import io
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
from PyQt5 import  QtGui, QtWidgets

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


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = QWebEngineView()
        self.view.setContentsMargins(50, 50, 50, 50)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QHBoxLayout(central_widget)

        lay.addWidget(self.view, stretch=1)

        m = folium.Map(location=[45.5236, -122.6750], tiles="Stamen Terrain", zoom_start=13)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

        self.setWindowTitle("Deneb")
        self.resize(1200, 500)
        self.disply_width = 500
        self.display_height = 500
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.textLabel = QLabel('RTSP stream')
        self.radio1 = QRadioButton("Otonom Kalkis")
        self.radio1.toggled.connect(self.kalkis)
        self.radio2 = QRadioButton("Otonom Inis")
        self.radio2.toggled.connect(self.inis)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)

        self.setLayout(vbox)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def kalkis(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            QMessageBox.about(self, "Title", "Message")

    def inis(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            QMessageBox.about(self, "Title", "Message")

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    a = App()
    a.show()
    sys.exit(app.exec_())
