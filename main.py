import requests
import sys
from services.weather_service import set_state, get_url
from ui.ui import print_weather, WeatherApp
from PyQt5.QtWidgets import QApplication

def main():
    state = ""
    city = ""

    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())

    while(True):
        state = input("Ingrese una provincia de Argentina: ")
        try:
            state = set_state(state)
            break
        except ValueError as error:
            print(error)

    while (True):
        city = input(f"Ingrese una ciudad de {state}: ").strip().lower()
        if city == "e":
            break

        try:
            url = get_url(city)
            response = requests.get(url)
            #print(response)
            response.raise_for_status()
            data = response.json()
            #print(data)
            print_weather(data)

        except ValueError as error:
            print(error)
        except requests.RequestException as error:
            print("API Error: ", error)

if __name__ == "__main__":
    main()