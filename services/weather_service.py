import json
from utils.loader import load_cities
from utils.normalizer import normalize_string
from utils.closest_match import closest_match

API_URL = "https://api.open-meteo.com/v1/forecast?"
CITIES_PATH = None 
CITIES = {}

def set_state(state: str) -> str:
    global CITIES_PATH, CITIES

    state = normalize_string(state)

    with open("states_map.json", "r", encoding="utf-8") as file:
        states_map = json.load(file)

    if state not in states_map:
        suggest = closest_match(state, list(states_map.keys()))
        if suggest:
            name = states_map.get(suggest).get('name')
            confirm = input(f"¿Quisiste decir '{name}'? (s/n): ").strip().lower()
            if confirm != "s":
                raise ValueError(f"State {state} is not in states_map.")
            state = suggest
        else:
            raise ValueError(f"State {state} is not in states_map.")

    CITIES_PATH = states_map.get(state).get("path")
    try:
        with open(CITIES_PATH, "r", encoding="utf-8") as file:
            CITIES = json.load(file)
            return states_map.get(state).get("name")
    except:
        raise ValueError(f"State '{state}' not found in local cities json base.")

def get_url(city: str) -> str:
    if not CITIES:
        raise ValueError(f"State not defined.")

    city_norm = normalize_string(city)

    if city_norm not in CITIES:
        suggest = closest_match(city_norm, list(CITIES.keys()))
        if suggest:
            name = CITIES.get(suggest).get('name')
            confirm = input(f"¿Quisiste decir '{name}'? (s/n): ").strip().lower()
            if confirm != "s":
                raise ValueError(f"City {city} is not in local cities json base.")
            city_norm = suggest
        else:
            raise ValueError(f"City {city} is not in local cities json base.")
    
    lat = CITIES[city_norm]["lat"]
    lon = CITIES[city_norm]["lon"]

    url = (
        f"{API_URL}latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )
    #print(url)
    return url
