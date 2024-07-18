# это код с учетом 4 задание(я потеряла где было чисто 3 так что ...)
import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QRadioButton,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MapManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.center = [0, 0]
        self.scale = 10
        self.map_size = (600, 450)
        self.min_longitude = -180
        self.max_longitude = 180
        self.min_latitude = -90
        self.max_latitude = 90

    def get_map_image(self, map_type):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(map(str, self.center))}&z={self.scale}&size={','.join(map(str, self.map_size))}&l={map_type}"
        response = requests.get(map_request)
        map_image = QPixmap()
        map_image.loadFromData(response.content)
        return map_image


class MapWidget(QWidget):
    def __init__(self, map_manager, parent=None):
        super().__init__(parent)
        self.map_manager = map_manager
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.scheme_radio = QRadioButton("Схема", self)
        self.satellite_radio = QRadioButton("Спутник", self)
        self.hybrid_radio = QRadioButton("Гибрид", self)
        self.coordinates_label = QLabel("Долгота, Широта:", self)
        self.coordinates_edit = QLineEdit(self)
        self.scale_label = QLabel("Масштаб 1-17:", self)
        self.scale_edit = QLineEdit(self)
        self.load_button = QPushButton("Загрузить Карту", self)
        self.label = QLabel(self)
        self.layout.addWidget(self.coordinates_label)
        self.layout.addWidget(self.coordinates_edit)
        self.layout.addWidget(self.scale_label)
        self.layout.addWidget(self.scale_edit)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scheme_radio)
        self.layout.addWidget(self.satellite_radio)
        self.layout.addWidget(self.hybrid_radio)
        # 
        self.load_button.clicked.connect(self.update_map)
        self.scheme_radio.setChecked(True)
        self.scheme_radio.toggled.connect(self.update_map)
        self.satellite_radio.toggled.connect(self.update_map)
        self.hybrid_radio.toggled.connect(self.update_map)
        self.setFocusPolicy(Qt.StrongFocus)

    def update_map(self):
        coordinates = self.coordinates_edit.text()
        scale = int(self.scale_edit.text())
        # if not (1 <= scale <= 17):
        #     raise ValueError("Масштаб должен быть от 1 до 17")
        map_type = "sat" if self.satellite_radio.isChecked() else "map"
        if self.hybrid_radio.isChecked():
            map_type = "skl"
        self.map_manager.scale = scale
        self.map_manager.center = [float(coord) for coord in coordinates.split(",")]
        map_image = self.map_manager.get_map_image(map_type)
        self.label.setPixmap(map_image)
        self.label.setScaledContents(True)
        # except Exception as e:
        #     QMessageBox.warning(self, "Ошибка", str(e))

    def handle_key_event(self, event):
        step = 5
        if (
            event.key() == Qt.Key_PageUp
            and self.map_manager.scale < self.map_manager.max_scale
        ):
            self.map_manager.scale += 1
        elif (
            event.key() == Qt.Key_PageDown
            and self.map_manager.scale > self.map_manager.min_scale
        ):
            self.map_manager.scale -= 1
        elif event.key() == Qt.Key_Up:
            new_latitude = self.map_manager.center[1] + step / self.map_manager.scale
            if (
                self.map_manager.min_latitude
                <= new_latitude
                <= self.map_manager.max_latitude
            ):
                self.map_manager.center[1] = new_latitude
        elif event.key() == Qt.Key_Down:
            new_latitude = self.map_manager.center[1] - step / self.map_manager.scale
            if (
                self.map_manager.min_latitude
                <= new_latitude
                <= self.map_manager.max_latitude
            ):
                self.map_manager.center[1] = new_latitude
        elif event.key() == Qt.Key_Right:
            new_longitude = self.map_manager.center[0] + step / self.map_manager.scale
            if (
                self.map_manager.min_longitude
                <= new_longitude
                <= self.map_manager.max_longitude
            ):
                self.map_manager.center[0] = new_longitude
        elif event.key() == Qt.Key_Left:
            new_longitude = self.map_manager.center[0] - step / self.map_manager.scale
            if (
                self.map_manager.min_longitude
                <= new_longitude
                <= self.map_manager.max_longitude
            ):
                self.map_manager.center[0] = new_longitude
        else:
            return
        self.update_map()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Я карта Я карта")
        self.setGeometry(100, 100, 600, 600)
        self.map_manager = MapManager(api_key="40d1649f-0493-4b70-98ba-98533de7710b")
        self.map_widget = MapWidget(self.map_manager, parent=self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.map_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())