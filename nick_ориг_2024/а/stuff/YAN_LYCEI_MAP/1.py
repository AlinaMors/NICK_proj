import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests


class MapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.coordinates_edit = QLineEdit(self)
        self.scale_edit = QLineEdit(self)
        self.load_button = QPushButton("Загрузить карту", self)
        self.label = QLabel(self)
        self.layout.addWidget(self.coordinates_edit)
        self.layout.addWidget(self.scale_edit)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.label)
        
        self.load_button.clicked.connect(self.show_map)

    def show_map(self):
        coordinates = self.coordinates_edit.text()
        scale = self.scale_edit.text()
        api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coordinates}&z={scale}&size=600,450&l=map"
        response = requests.get(map_request)
        if response.status_code == 200:
            map_image = QPixmap()
            map_image.loadFromData(response.content)
            self.label.setPixmap(map_image)
            self.label.setScaledContents(True)
        else:
            print("упссс")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Я Карта, Я карта")
        self.setGeometry(100, 100, 600, 500)
        self.map_widget = MapWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.map_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
 