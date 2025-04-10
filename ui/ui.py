def print_weather(data: dict):

    if "current_weather" not in data:
        print("API did not return current weather.")
        print("API's answer: ", data)
        return
    
    weather = data.get("current_weather", {})
    print(f"Temperatura: {weather.get('temperature')}°C")
    print(f"Viento: {weather.get('windspeed')} km/h")
    print(f"Dirección del viento: {weather.get('winddirection')}°")