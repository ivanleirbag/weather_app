import sys
from services.weather_service import *
from ui.weather_app import WeatherApp
from PyQt5.QtWidgets import QApplication

def main():
    state = "Entre Ríos"
    city = "Concordia"

    set_state(state)
    weather = get_weather_for_city(city)

    app = QApplication(sys.argv)
    window = WeatherApp(city, 
                        weather.get('temperature'), 
                        weather.get('windspeed'), 
                        weather.get('winddirection'),
                        weather.get('is_day'))
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()