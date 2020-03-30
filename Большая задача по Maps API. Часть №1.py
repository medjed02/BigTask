from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import sys
import os
import requests


class pil2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global map_file
        toponym_longitude, toponym_lattitude = '43.820637', '56.364506'
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

        self.setGeometry(400, 400, 600, 450)

        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = pil2()
    ex.show()
    os.remove(map_file)
    sys.exit(app.exec())