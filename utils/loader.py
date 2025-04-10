import json
import os

def load_cities(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)