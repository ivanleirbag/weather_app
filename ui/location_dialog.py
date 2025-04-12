from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox, QCompleter
from PyQt5.QtCore import Qt
from services.weather_service import *

class LocationDialog(QDialog):
    """
    Dialog for selecting a location (state and city) and retrieving weather data.

    Provides a UI with a combo box for selecting a province (state) and another one for a city city,
    and fetches weather data for the selected city. Allows the user to confirm their selection
    and accept the new location.
    """
    def __init__(self, parent=None):
        """
        Initialize the location selection dialog.

        Args:
            parent (QWidget, optional): The parent widget for this dialog.
        """
        super().__init__(parent)
        self.weather = {}
        self.setWindowTitle("Seleccionar ubicación")
        self.selected_province = None
        self.selected_city = None
        self.states = get_states()
        
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Provincia:"))
        self.states_combo = QComboBox()
        self.states_combo.setEditable(True)
        self.states_combo.addItems(self.states.keys())
        self.states_combo.activated[str].connect(self.update_cities)
        layout.addWidget(self.states_combo)
        self.states_completer = QCompleter(self.states.keys())
        self.states_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.states_completer.setFilterMode(Qt.MatchContains)
        self.states_combo.setCompleter(self.states_completer)

        layout.addWidget(QLabel("Ciudad:"))
        self.city_combo = QComboBox()
        self.city_combo.setEditable(True)
        layout.addWidget(self.city_combo)
        self.city_completer = QCompleter()
        self.city_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.city_completer.setFilterMode(Qt.MatchContains)
        self.city_combo.setCompleter(self.city_completer)

        self.accept_btn = QPushButton("Aceptar")
        self.accept_btn.clicked.connect(self.on_Accept)
        layout.addWidget(self.accept_btn)

        self.setLayout(layout)
        self.update_cities(self.states_combo.currentText())

    def update_cities(self, state):
        """
        Updates the list of cities based on the selected state.

        Args:
            state (str): The selected state.
        """
        set_state(state)
        self.city_combo.clear()
        self.city_combo.addItems(get_cities())
        self.city_completer.setModel(self.city_combo.model())

    def get_city(self) -> str:
        """
        Returns the selected city.

        Returns:
            str: The name of the selected city.
        """
        return self.city_combo.currentText()
    
    def get_state(self) -> str:
        """
        Returns the selected state.

        Returns:
            str: The name of the selected state.
        """
        return self.states_combo.currentText()

    def on_Accept(self):
        """
        Accepts the selected location and fetches the weather data for the selected city.
        If weather data is successfully retrieved, the dialog is accepted. 
        Otherwise, an error message is displayed.
        """
        set_state(self.get_state())
        self.weather = get_weather_for_city(self.get_city())

        if self.weather:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "No se pudo obtener el clima para esta ciudad.")

    def get_new_weather(self) -> dict:
        """
        Returns the fetched weather data for the selected city.

        Returns:
            dict: The weather data for the selected city.
        """
        return self.weather
