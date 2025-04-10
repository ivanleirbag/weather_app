import json
import requests
from unidecode import unidecode

# URL del archivo de localidades
url = 'https://apis.datos.gob.ar/georef/api/localidades?provincia=06&campos=nombre,centroide&max=5000'

# Descargar el archivo de localidades
response = requests.get(url)
if response.status_code != 200:
    raise Exception("No se pudo descargar el archivo de localidades.")

localidades = response.json()['localidades']

# Diccionario para almacenar las ciudades de Buenos Aires
buenos_aires = {}

# Función para normalizar nombres
def normalize_name(name):
    return unidecode(name).lower().replace(' ', '')

# Procesar cada localidad
for localidad in localidades:
    nombre_ciudad = localidad['nombre']
    lat = localidad['centroide']['lat']
    lon = localidad['centroide']['lon']

    # Normalizar el nombre de la ciudad
    nombre_ciudad_normalizado = normalize_name(nombre_ciudad)

    # Añadir la ciudad al diccionario
    buenos_aires[nombre_ciudad_normalizado] = {
        'nombre': nombre_ciudad,
        'lat': lat,
        'lon': lon
    }

# Guardar el diccionario en un archivo JSON
with open('buenos_aires.json', 'w', encoding='utf-8') as f:
    json.dump(buenos_aires, f, ensure_ascii=False, indent=4)

print("Archivo 'buenos_aires.json' generado con éxito.")
