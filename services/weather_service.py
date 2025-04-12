import json
import requests

API_URL = "https://api.open-meteo.com/v1/forecast?"
CITIES_PATH = None 
CITIES = {}
url = ""

def set_state(state: str) -> str:
    """
    Sets the active country state and loads the corresponding city data from a local JSON file.

    Args:
        state (str): The name of the state to set.

    Raises:
        ValueError: If the state is not found in the local cities JSON base.
    """
    global CITIES_PATH, CITIES

    with open("states_map.json", "r", encoding="utf-8") as file:
        states_map = json.load(file)

    CITIES_PATH = states_map.get(state)
    try:
        with open(CITIES_PATH, "r", encoding="utf-8") as file:
            CITIES = json.load(file)
    except:
        raise ValueError(f"WS: State '{state}' not found in local cities json base.")

def get_states()->dict:
    """
    Returns:
        dict: A dictionary mapping state's names to file paths.
    """
    with open("states_map.json", "r", encoding="utf-8") as file:
        states_map = json.load(file)
    return states_map

def get_cities()->list[str]:
    """
    Retrieves a list of available cities for the current state.

    Returns:
        list[str]: A list of city names.
    """
    return list(CITIES.keys())

def set_url(city: str):
    """
    Builds the API URL for the given city based on its latitude and longitude.

    Args:
        city (str): The name of the city.

    Raises:
        ValueError: If no state is currently defined or the city is not available.
    """
    global url, CITIES
    if not CITIES:
        raise ValueError(f"WS: State not defined.")
    
    lat = CITIES[city]["lat"]
    lon = CITIES[city]["lon"]

    url = (
        f"{API_URL}latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )

def get_weather_for_city(city: str) -> dict:
    """
    Retrieves the current weather for the specified city using the open-meteo API.

    Args:
        city (str): The name of the city.

    Returns:
        dict: A dictionary containing current weather data.

    Raises:
        ValueError: If the API does not return valid weather data.
    """
    set_url(city)
    response = requests.get(url)
    weather = response.json().get("current_weather", {})
    if weather:
        return weather
    else:
        raise ValueError(f"WS: Didn't get data from API.")
