from PyQt5.QtWidgets import (
    QDialog, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from services.weather_service import *
from ui.location_dialog import LocationDialog


class WeatherApp(QWidget):
    """
    Main weather application widget.

    Displays current weather data including temperature, wind speed, and wind direction,
    with an icon representing weather conditions based on temperature and time of day.
    Allows changing the city via a dialog.
    """
    def __init__(self, city: str, temp: float, wind_speed: int, wind_dir: int, is_day: int):
        """
        Initialize the weather application UI.

        Args:
            city (str): The name of the city.
            temp (float): The current temperature in Celsius.
            wind_speed (int): Wind speed in km/h.
            wind_dir (int): Wind direction in degrees.
            is_day (int): 1 if it is daytime, 0 if it is nighttime.
        """
        super().__init__()
        self.city = city
        self.temp = temp
        self.wind_speed = wind_speed
        self.wind_dir = wind_dir
        self.is_day = is_day
        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI components of the application.
        Creates and arranges labels, icons, and buttons to display weather data.
        """
        self.setWindowTitle("App del Clima")
        self.setGeometry(200, 200, 400, 350)

        main_layout = QVBoxLayout()

        #--Data layout--#
        top_layout = QHBoxLayout()

        #--Weather icon--#
        self.weather_icon = QSvgWidget()
        self.set_weather_icon()
        top_layout.addWidget(self.weather_icon, alignment=Qt.AlignCenter)

        #--Weather data grid--#
        data_layout = QGridLayout()

        self.city_label = QLabel(self.city)
        self.city_label.setFont(QFont("Arial", 14))
        self.city_label.setAlignment(Qt.AlignCenter)

        self.temp_label = QLabel(f"{self.temp}°C")
        self.temp_label.setFont(QFont("Arial", 40))

        self.ws_icon = QSvgWidget("assets/wind.svg")
        self.ws_icon.setFixedSize(100, 100)

        self.ws_label = QLabel(f"{self.wind_speed}km/h")
        self.ws_label.setFont(QFont("Arial", 12))

        self.wd_icon = QSvgWidget("assets/direction.svg")
        self.wd_icon.setFixedSize(50, 50)

        self.wd_label = QLabel(f"{self.wind_dir}°")
        self.wd_label.setFont(QFont("Arial", 12))

        data_layout.addWidget(self.city_label, 0, 0, 1, 2, Qt.AlignCenter)
        data_layout.addWidget(self.temp_label, 1, 0, 1, 2, Qt.AlignCenter)
        data_layout.addWidget(self.ws_icon, 2, 0, alignment=Qt.AlignCenter)
        data_layout.addWidget(self.wd_icon, 2, 1, alignment=Qt.AlignCenter)
        data_layout.addWidget(self.ws_label, 3, 0, alignment=Qt.AlignCenter)
        data_layout.addWidget(self.wd_label, 3, 1, alignment=Qt.AlignCenter)

        top_layout.addLayout(data_layout)

        #--Button--#
        self.change_city_btn = QPushButton("Cambiar ciudad")
        self.change_city_btn.clicked.connect(self.change_location)
        self.change_city_btn.setFixedHeight(40)
        self.change_city_btn.setStyleSheet("font-size: 16px;")

        main_layout.addLayout(top_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(self.change_city_btn)

        self.setLayout(main_layout)

    def change_location(self):
        """
        Opens a dialog to change the city.
        If a new location is selected and valid weather data is returned,
        updates the internal state and refreshes the UI.
        """
        dialog = LocationDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.get_new_weather():
            self.weather = dialog.get_new_weather()
            #print(self.weather)
            self.city = dialog.get_city()
            self.temp = self.weather.get('temperature')
            self.wind_speed = self.weather.get('windspeed')
            self.wind_dir = self.weather.get('winddirection')
            self.is_day = self.weather.get('is_day')
            self.refresh_ui()
        
    def refresh_ui(self):
        """
        Updates the UI elements with the current weather data.
        Refreshes labels and weather icons based on updated values.
        """
        self.city_label.setText(self.city)
        self.temp_label.setText(f"{self.temp}°C")
        self.ws_label.setText(f"{self.wind_speed}km/h")
        self.wd_label.setText(f"{self.wind_dir}°")
        self.set_weather_icon()

    def set_weather_icon(self):
        """
        Sets the appropriate weather icon based on the temperature and whether it's day or night.
        Loads the icon as an SVG and displays it in the UI.
        """
        path = "assets/"
        temp = int(self.temp)
        if temp <= 15:
            path = path + "frost"
        elif temp > 15 and temp <=23:
            path = path + "cloudy"
        else:
            path = path + "clear"

        if self.is_day == 1:
            path = path + "-day.svg"
        else:
            path = path + "-night.svg"

        self.weather_icon = QSvgWidget(path)
        self.weather_icon.setFixedSize(200, 170)