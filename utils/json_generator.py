import json
import requests
from unidecode import unidecode

prov_name = "cordoba"
prov_id = "14"
url = f'https://apis.datos.gob.ar/georef/api/localidades?provincia={prov_id}&campos=nombre,centroide&max=5000'

response = requests.get(url)
if response.status_code != 200:
    raise Exception("No se pudo descargar el archivo de localidades.")

localidades = response.json()['localidades']

provincia = {}

def normalize_name(name):
    return unidecode(name).lower().replace(' ', '')

for localidad in localidades:
    nombre_ciudad = localidad['nombre']
    lat = localidad['centroide']['lat']
    lon = localidad['centroide']['lon']

    #nombre_ciudad_normalizado = normalize_name(nombre_ciudad)

    provincia[nombre_ciudad] = {
        'lat': lat,
        'lon': lon
    }

file_name = f"cities/{prov_name}.json"
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(provincia, f, ensure_ascii=False, indent=4)

print("Archivo json generado con éxito.")
