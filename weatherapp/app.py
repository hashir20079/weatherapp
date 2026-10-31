from flask import Flask, render_template, request
import requests
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
EMBEDDED_API_KEY = "6632e6327ad22276ac3b9ee2cbdc158e"

def format_city_local_time(timestamp, tz_offset_seconds):
    """
    Converts a Unix timestamp into the specific city's local time string,
    incorporating the city's UTC timezone offset.
    """
    if not timestamp:
        return "N/A"
    city_time = datetime.fromtimestamp(timestamp, tz=timezone.utc) + timedelta(seconds=tz_offset_seconds)
    return city_time.strftime("%I:%M %p").lstrip("0")

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data_list = []
    error_message = None
    
    if request.method == 'POST':
        cities_input = request.form.get('cities', '').strip()
        
        if not cities_input:
            error_message = "At least one city name is required."
        else:
            cities = [c.strip() for c in cities_input.split(',') if c.strip()]
            if len(cities) < 1 or len(cities) > 3:
                error_message = "Please enter between 1 and 3 cities."
            else:
                for city_name in cities:
                    params = {
                        "q": city_name,
                        "appid": EMBEDDED_API_KEY,
                        "units": "metric"
                    }
                    try:
                        response = requests.get(BASE_URL, params=params)
                        data = response.json()
                        if response.status_code == 200:
                            temp = data["main"]["temp"]
                            wind = data["wind"]["speed"]
                            humidity = data["main"]["humidity"]
                            tz_offset = data.get("timezone", 0)  # Offset from UTC in seconds
                            
                            # Calculate current time in the target city's timezone
                            now_utc = datetime.now(timezone.utc)
                            city_now = now_utc + timedelta(seconds=tz_offset)
                            city_local_time_str = city_now.strftime("%I:%M %p").lstrip("0")
                            
                            # Calculate timezone display label
                            tz_hours = tz_offset / 3600
                            tz_label = f"UTC{'+' if tz_hours >= 0 else ''}{int(tz_hours) if tz_hours.is_integer() else tz_hours}"

                            # Hourly forecast curves
                            hours = ["9 AM", "12 PM", "3 PM", "6 PM", "9 PM", "12 AM", "3 AM", "6 AM"]
                            forecast_temps = [
                                round(temp - 2, 1),
                                round(temp, 1),
                                round(temp - 1, 1),
                                round(temp - 3, 1),
                                round(temp - 5, 1),
                                round(temp - 6, 1),
                                round(temp - 6.5, 1),
                                round(temp - 6, 1)
                            ]
                            alt1 = [t + 1.2 for t in forecast_temps]
                            alt2 = [t - 1.5 for t in forecast_temps]
                            
                            icon_code = data["weather"][0]["icon"] if data.get("weather") else "02d"

                            weather_data_list.append({
                                "success": True,
                                "city": data["name"],
                                "country": data["sys"]["country"],
                                "temp": temp,
                                "feels_like": data["main"]["feels_like"],
                                "humidity": humidity,
                                "description": data["weather"][0]["description"].capitalize(),
                                "wind_speed": wind,
                                "local_time": city_local_time_str,
                                "tz_label": tz_label,
                                "sunrise": format_city_local_time(data["sys"].get("sunrise"), tz_offset),
                                "sunset": format_city_local_time(data["sys"].get("sunset"), tz_offset),
                                "water": round(temp - 4, 2),
                                "icon": icon_code,
                                "chart_hours": hours,
                                "chart_temps": forecast_temps,
                                "chart_alt1": alt1,
                                "chart_alt2": alt2
                            })
                        else:
                            weather_data_list.append({
                                "success": False,
                                "city": city_name,
                                "error": data.get("message", "City not found.")
                            })
                    except Exception as e:
                        weather_data_list.append({
                            "success": False,
                            "city": city_name,
                            "error": str(e)
                        })
                        
    return render_template('index.html', weather_data=weather_data_list, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)