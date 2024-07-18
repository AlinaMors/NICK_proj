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


class I_am_ystal:
    def __init__(self, api_key):
        self.api_key = api_key
        self.center = [0, 0]
        self.scale = 10
        self.map_size = (600, 450)
        self.markers = []

    def add_marker(self, longitude, latitude):
        self.markers.append((longitude, latitude))

    def get_map_image(self, map_type):
        markers_str = "~".join([f"{lon},{lat},comma" for lon, lat in self.markers])
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(map(str, self.center))}&z={self.scale}&size={','.join(map(str, self.map_size))}&l={map_type}&pt={markers_str}"
        response = requests.get(map_request)
        if response.status_code != 200:
            raise ValueError("Failed to fetch map.")
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
        self.coordinates_label = QLabel("Координаты (Долгота, Широта):", self)
        self.coordinates_edit = QLineEdit(self)
        self.scale_label = QLabel("Масштаб (1-17):", self)
        self.scale_edit = QLineEdit(self)
        self.load_button = QPushButton("Загрузить Карту", self)
        self.label = QLabel(self)
        self.scheme_radio = QRadioButton("Схема", self)
        self.satellite_radio = QRadioButton("Спутник", self)
        self.hybrid_radio = QRadioButton("Гибрид", self)
        self.search_label = QLabel("Поиск объекта:", self)
        self.search_edit = QLineEdit(self)
        self.search_button = QPushButton("Искать", self)

        # туц туц новый код:  
        self.clear_button = QPushButton("Сброс результата", self)
        self.layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_search_result)  

        self.layout.addWidget(self.coordinates_label)
        self.layout.addWidget(self.coordinates_edit)
        self.layout.addWidget(self.scale_label)
        self.layout.addWidget(self.scale_edit)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scheme_radio)
        self.layout.addWidget(self.satellite_radio)
        self.layout.addWidget(self.hybrid_radio)
        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_edit)
        self.layout.addWidget(self.search_button)
        self.load_button.clicked.connect(self.update_map)
        self.scheme_radio.setChecked(True)
        self.scheme_radio.toggled.connect(self.update_map)
        self.satellite_radio.toggled.connect(self.update_map)
        self.hybrid_radio.toggled.connect(self.update_map)
        self.search_button.clicked.connect(self.search_object)
        self.setFocusPolicy(Qt.StrongFocus)

    def update_map(self):
        try:
            coordinates = self.coordinates_edit.text()
            scale = int(self.scale_edit.text())
            if not (1 <= scale <= 17):
                raise ValueError("Масштаб 1 до 17")
            map_type = "sat" if self.satellite_radio.isChecked() else "map"
            if self.hybrid_radio.isChecked():
                map_type = "skl"
            self.map_manager.scale = scale
            self.map_manager.center = [float(coord) for coord in coordinates.split(",")]
            markers = self.map_manager.markers
            map_image = self.map_manager.get_map_image(map_type)
            for lon, lat in markers:
                self.map_manager.add_marker(lon, lat)

            self.label.setPixmap(map_image)
            self.label.setScaledContents(True)
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Произошла непредвиденная ошибка.")

    def search_object(self):
        try:
            search_query = self.search_edit.text()
            if not search_query:
                raise ValueError("Введите запрос для поиска объекта")

            response = requests.get(
                f"https://geocode-maps.yandex.ru/1.x/?apikey={self.map_manager.api_key}&format=json&geocode={search_query}"
            )
            if response.status_code != 200:
                raise ValueError(
                    "Не удалось выполнить поиск. Пожалуйста, попробуйте позже."
                )

            response_data = response.json()
            found_objects = response_data["response"]["GeoObjectCollection"][
                "featureMember"
            ]
            if not found_objects:
                raise ValueError("Объект не найден")

            coordinates_str = found_objects[0]["GeoObject"]["Point"]["pos"]
            coordinates = [float(coord) for coord in coordinates_str.split()]
            self.coordinates_edit.setText(",".join(map(str, coordinates)))
            self.update_map()
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Произошла непредвиденная ошибка.")

# Супер-НОВЫЙ КОД чееек
    def clear_search_result(self):
        self.map_manager.markers = []
        self.update_map()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 600)
        self.map_manager = I_am_ystal(api_key="40d1649f-0493-4b70-98ba-98533de7710b")
        self.map_widget = MapWidget(self.map_manager, parent=self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.map_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
