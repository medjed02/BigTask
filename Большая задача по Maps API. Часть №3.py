from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import requests


class BigTask(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.start_longitube = 43.820637
        self.start_lattitude = 56.364506
        self.max_longitube = 179.9936
        self.min_longitube = -179.9936
        self.max_lattitude = 85.0801
        self.min_lattitude = -85.0801
        self.setGeometry(100, 100, 600, 450)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.make_image(str(self.start_longitube), str(self.start_lattitude))

    def make_image(self, toponym_longitude, toponym_lattitude):
        global map_file
        delta = "0.005"
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map"}
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap('map.png')
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            self.start_lattitude += 0.00535
            if self.start_lattitude > self.max_lattitude:
                self.start_lattitude = self.max_lattitude
        elif e.key() == Qt.Key_Down:
            self.start_lattitude -= 0.00535
            if self.start_lattitude < self.min_lattitude:
                self.start_lattitude = self.min_lattitude
        elif e.key() == Qt.Key_Right:
            self.start_longitube += 0.0128
            if self.start_longitube > self.max_longitube:
                self.start_longitube = self.max_longitube
        elif e.key() == Qt.Key_Left:
            self.start_longitube -= 0.0128
            if self.start_longitube < self.min_longitube:
                self.start_longitube = self.min_longitube
        self.make_image(str(self.start_longitube), str(self.start_lattitude))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BigTask()
    ex.show()
    os.remove(map_file)
    sys.exit(app.exec())