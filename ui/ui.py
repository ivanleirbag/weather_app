from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


def print_weather(data: dict):

    if "current_weather" not in data:
        print("API did not return current weather.")
        print("API's answer: ", data)
        return
    
    weather = data.get("current_weather", {})
    print(f"Temperatura: {weather.get('temperature')}°C")
    print(f"Viento: {weather.get('windspeed')} km/h")
    print(f"Dirección del viento: {weather.get('winddirection')}°")


from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("App del Clima")
        self.setGeometry(200, 200, 600, 300)

        main_layout = QVBoxLayout()

        # 1. Layout superior (ícono de clima y datos)
        top_layout = QHBoxLayout()

        # Ícono del clima
        self.weather_icon = QLabel()
        pixmap = QPixmap("weather_icons/sun_cloud.png")  # Asegurate de tener esta imagen
        self.weather_icon.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        top_layout.addWidget(self.weather_icon)

        # Grid con datos: ciudad, temperatura, viento
        data_layout = QGridLayout()

        self.city_label = QLabel("Concordia")
        self.city_label.setFont(QFont("Arial", 14))
        self.city_label.setAlignment(Qt.AlignCenter)

        self.temp_label = QLabel("19°C")
        self.temp_label.setFont(QFont("Arial", 40))

        self.wind_icon = QLabel("🌬️")  # Alternativamente un ícono
        self.wind_speed = QLabel("10 km/h")
        self.wind_dir_icon = QLabel("↗")
        self.wind_deg = QLabel("39°")

        data_layout.addWidget(self.city_label, 0, 0, 1, 2, Qt.AlignCenter)
        data_layout.addWidget(self.temp_label, 1, 0, 1, 2, Qt.AlignCenter)
        data_layout.addWidget(self.wind_icon, 2, 0)
        data_layout.addWidget(self.wind_dir_icon, 2, 1)
        data_layout.addWidget(self.wind_speed, 3, 0)
        data_layout.addWidget(self.wind_deg, 3, 1)

        top_layout.addLayout(data_layout)

        # 2. Botón para cambiar ciudad
        self.change_city_btn = QPushButton("Cambiar ciudad")
        self.change_city_btn.setFixedHeight(40)
        self.change_city_btn.setStyleSheet("font-size: 16px;")

        # Espaciador para estética
        main_layout.addLayout(top_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(self.change_city_btn)

        self.setLayout(main_layout)