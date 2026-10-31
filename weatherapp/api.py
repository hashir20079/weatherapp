import requests
from datetime import datetime
from config import BASE_URL

def format_time(timestamp):
    """Converts a Unix timestamp to a 12-hour AM/PM time string."""
    if not timestamp:
        return "N/A"
    return datetime.fromtimestamp(timestamp).strftime("%I:%M %p").lstrip("0")

def fetch_weather_data(cities, api_key):
    """
    Takes a list of city names and the API key, queries the API for each,
    and returns a list of result dictionaries containing weather data or errors.
    """
    results = []
    for city_name in cities:
        params = {
            "q": city_name,
            "appid": api_key,
            "units": "metric"
        }
        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            
            if response.status_code == 200:
                results.append({
                    "success": True,
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "wind_speed": data["wind"]["speed"],
                    "sunrise": format_time(data["sys"].get("sunrise")),
                    "sunset": format_time(data["sys"].get("sunset"))
                })
            elif response.status_code == 404:
                results.append({
                    "success": False,
                    "city": city_name,
                    "error": "City not found. Please check spelling."
                })
            else:
                results.append({
                    "success": False,
                    "city": city_name,
                    "error": f"Server responded with code {response.status_code}."
                })
                
        except requests.exceptions.RequestException as e:
            results.append({
                "success": False,
                "city": city_name,
                "error": f"Network error: {e}"
            })
            
    return results