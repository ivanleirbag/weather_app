import json
import os
from utils.loader import load_cities
from utils.normalizer import normalize_string

API_URL = "https://api.open-meteo.com/v1/forecast?"
CITIES_PATH = None #os.path.join("cities", "entre_rios.json")
CITIES = {}

def set_state(state: str):
    global CITIES_PATH, CITIES

    state = normalize_string(state)

    with open("states_map.json", "r", encoding="utf-8") as file:
        states_map = json.load(file)

    if state not in states_map:
        raise ValueError(f"State {state} is not in states_map.")

    CITIES_PATH = states_map[state]
    try:
        with open(CITIES_PATH, "r", encoding="utf-8") as file:
            CITIES = json.load(file)
    except:
        raise ValueError(f"State '{state}' not found in local cities json base.")

def get_url(city: str) -> str:
    if not CITIES:
        raise ValueError(f"State not defined.")

    city = normalize_string(city)

    if city not in CITIES:
        raise ValueError(f"City '{city}' not found in local cities json base.")
    
    lat = CITIES[city]["lat"]
    lon = CITIES[city]["lon"]

    url = (
        f"{API_URL}latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )
    #print(url)
    return url
