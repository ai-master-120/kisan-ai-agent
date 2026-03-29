import requests


def get_weather(city="Chandigarh"):
    # Step 1 - Get coordinates of the city
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    location = requests.get(url).json()

    lat = location['results'][0]['latitude']
    lon = location['results'][0]['longitude']

    # Step 2 - Get current weather + 7 day forecast
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=precipitation_sum,weathercode,windspeed_10m_max&timezone=Asia/Kolkata&forecast_days=7"

    weather = requests.get(weather_url).json()

    # Current weather
    current = weather['current_weather']
    result = f"Current Temperature: {current['temperature']}°C, Wind: {current['windspeed']} km/h\n"
    result += "\n📅 7-Day Forecast:\n"

    # Weather codes meaning
    def describe_weather(code):
        if code == 0:
            return "☀️ Clear sky"
        elif code in [1, 2, 3]:
            return "⛅ Partly cloudy"
        elif code in [51, 53, 55, 61, 63, 65]:
            return "🌧️ Rain expected"
        elif code in [71, 73, 75]:
            return "❄️ Snow"
        elif code in [95, 96, 99]:
            return "⛈️ Thunderstorm - Protect your crops!"
        else:
            return "🌤️ Mixed weather"

    # Loop through 7 days
    dates = weather['daily']['time']
    rain = weather['daily']['precipitation_sum']
    codes = weather['daily']['weathercode']
    wind = weather['daily']['windspeed_10m_max']

    for i in range(7):
        result += f"{dates[i]}: {describe_weather(codes[i])}, Rain: {rain[i]}mm, Wind: {wind[i]} km/h\n"

    return result


print(get_weather("Ludhiana"))