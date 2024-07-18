import sys
import requests
from geopy.distance import geodesic

from math import cos, sin, atan2, sqrt, radians
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QRadioButton,
    QCheckBox,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MapManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.center = [0, 0]
        self.scale = 10
        self.map_size = (600, 450)
        self.markers = []

    def add_marker(self, longitude, latitude):
        self.markers.append((longitude, latitude))

    def get_map_image(self, map_type):
        try:
            markers_str = "~".join([f"{lon},{lat},comma" for lon, lat in self.markers])
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(map(str, self.center))}&z={self.scale}&size={','.join(map(str, self.map_size))}&l={map_type}&pt={markers_str}"
            response = requests.get(map_request)
            response.raise_for_status()
            map_image = QPixmap()
            map_image.loadFromData(response.content)
            return map_image
        except requests.RequestException as e:
            raise Exception("Error fetching map image:", e)

class MapWidget(QWidget):
    def __init__(self, map_manager, parent=None):
        super().__init__(parent)
        self.map_manager = map_manager
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.load_button = QPushButton("Map", self)
        self.layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.update_map)

    def update_map(self):
        map_image = self.map_manager.get_map_image("map")
        self.label.setPixmap(map_image)
        self.label.setScaledContents(True)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_thing(event, self.search_object)
        elif event.button() == Qt.RightButton:
            self.mouse_thing(event, self.search_organization)

    def mouse_thing(self, event, search_function):
        pos_find = event.pos()
        map_size = self.label.size()
        lon = (pos_find.x() / map_size.width()) * 360 - 180
        lat = 90 - (pos_find.y() / map_size.height()) * 180
        self.clear_Results()
        self.map_manager.markers = [(lon, lat)]
        search_function(lon, lat)
        self.update_map()

    def search_organization(self, lon, lat):
        try:
            response = requests.get(
                f"https://search-maps.yandex.ru/v1/?text=organization&ll={lon},{lat}&spn=0.001,0.001&apikey={self.map_manager.api_key}"
            )
            response.raise_for_status()
            response_data = response.json()
            found_organizations = response_data.get("features", [])
            if found_organizations:
                first_organization = found_organizations[0]
                organization_lon, organization_lat = first_organization["geometry"]["coordinates"]
                distance = self.distance_answer(lon, lat, organization_lon, organization_lat)
                if distance <= 50:
                    self.found_objects = [first_organization]
                    self.update_address(self.found_objects)
                    QMessageBox.warning(self, "Error", "Рядом нет организаций")
        except requests.RequestException as e:
            QMessageBox.warning(self, "Error")

    def distance_answer(self, lon1, lat1, lon2, lat2):
        a = (lat1, lon1)
        b = (lat2, lon2)
        return geodesic(a, b).meters

    def clear_Results(self):
        self.found_objects = []
        self.address_display.clear()
s
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 600)
        self.map_manager = MapManager(
            api_key="40d1649f-0493-4b70-98ba-98533de7710b"
        )
        self.map_widget = MapWidget(self.map_manager, parent=self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.map_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
