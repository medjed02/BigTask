from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
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
        self.setGeometry(300, 50, 1200, 950)

        self.toponym_text = QLineEdit(self)
        self.toponym_text.resize(500, 30)
        self.toponym_text.move(180, 910)
        self.toponym_text.setDisabled(True)

        self.btn1 = QPushButton('Начать набор текста', self)
        self.btn1.resize(150, 40)
        self.btn1.move(15, 905)
        self.btn1.clicked.connect(self.start_text)

        self.btn2 = QPushButton('Искать!', self)
        self.btn2.resize(150, 40)
        self.btn2.move(710, 905)
        self.btn2.clicked.connect(self.find_toponym)
        self.btn2.setDisabled(True)

        self.label = QLabel(self)
        self.label.setText("")
        self.label.resize(110, 30)
        self.label.move(980, 910)

        # Перемещать центр карты на W, S, D, A вверх, вниз, вправо и влево соответственно
        self.start_longitube = 43.820637
        self.start_lattitude = 56.364506
        self.max_longitube = 180
        self.min_longitube = -180
        self.max_lattitude = 90
        self.min_lattitude = -90
        self.right_border = 43.824742
        self.up_border = 56.366784
        self.left_border = 43.816532
        self.down_border = 56.362227
        self.point = False

        # Масштаб меняется на PgUp/PgDown
        self.delta = 0.005

        # Слой меняется на кнопку L
        self.layer = "sat"

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(1200, 900)
        self.make_image()

    def start_text(self):
        self.toponym_text.setDisabled(False)
        self.btn2.setDisabled(False)

    def mousePressEvent(self, QMouseEvent):
        self.toponym_text.setDisabled(True)
        self.btn2.setDisabled(True)

    def make_image(self):
        global map_file
        map_params = {
            "ll": ",".join([str(self.start_longitube), str(self.start_lattitude)]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": self.layer}
        if self.point:
            map_params["pt"] = f"{self.point_longitube},{self.point_lattitude},pm2rdl1"
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if self.layer == "map":
            map_file = "map.png"
        else:
            map_file = "map.jpg"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(map_file)
        self.image.setPixmap(self.pixmap.scaled(1200, 900))

    def find_toponym(self):
        toponym_to_find = self.toponym_text.text()
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        found = json_response['response']['GeoObjectCollection']['metaDataProperty'][
            'GeocoderResponseMetaData']['found']
        if not response or found == '0':
            self.label.setText("Объект не найден")
        else:
            self.label.setText("")
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            toponym_coordinates = toponym["Point"]["pos"]
            toponym_corners = toponym["boundedBy"]["Envelope"]
            self.start_longitude, self.start_lattitude = [float(i) for i in toponym_coordinates.split(" ")]
            self.right_border, self.up_border = [float(i) for i in toponym_corners["upperCorner"].split(" ")]
            self.left_border, self.down_border = [float(i) for i in toponym_corners["lowerCorner"].split(" ")]
            self.point = True
            self.point_longitube, self.point_lattitude = self.start_longitude, self.start_lattitude
            self.make_image()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_W or e.key() == 1062:
            self.start_lattitude += self.delta
            if self.start_lattitude > self.max_lattitude - self.delta / 2:
                self.start_lattitude = self.max_lattitude - self.delta / 2
        elif e.key() == Qt.Key_S or e.key() == 1067:
            self.start_lattitude -= self.delta
            if self.start_lattitude < self.min_lattitude + self.delta / 2:
                self.start_lattitude = self.min_lattitude + self.delta / 2
        elif e.key() == Qt.Key_D or e.key() == 1042:
            self.start_longitube += self.delta * 2
            if self.start_longitube > self.max_longitube - self.delta:
                self.start_longitube = self.max_longitube - self.delta
        elif e.key() == Qt.Key_A or e.key() == 1060:
            self.start_longitube -= self.delta * 2
            if self.start_longitube < self.min_longitube + self.delta:
                self.start_longitube = self.min_longitube + self.delta
        elif e.key() == Qt.Key_PageUp:
            self.delta = min(90, self.delta * 2)
        elif e.key() == Qt.Key_PageDown:
            self.delta = max(0.001, self.delta / 2)
        elif e.key() == Qt.Key_L or e.key() == 1044:
            layers = ["map", "sat", "sat,skl"]
            self.layer = layers[(layers.index(self.layer) + 1) % 3]
        self.make_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BigTask()
    ex.show()
    if "map.jpg" in os.listdir():
        os.remove("map.jpg")
    if "map.png" in os.listdir():
        os.remove("map.png")
    sys.exit(app.exec())