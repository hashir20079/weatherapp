# display.py

def display_weather_data(results):
    """
    Takes the fetched weather results and renders them into a clean terminal UI.
    """
    print("\n" + "=" * 50)
    print(" 🌤️  WEATHER FORECAST REPORT")
    print("=" * 50)
    
    for res in results:
        if res["success"]:
            print(f"\n📍 {res['city']}, {res['country']}")
            print(f" • Condition   : {res['description']}")
            print(f" • Temperature : {res['temp']}°C (Feels like {res['feels_like']}°C)")
            print(f" • Humidity    : {res['humidity']}%")
            print(f" • Wind Speed  : {res['wind_speed']} m/s")
        else:
            print(f"\n❌ [Error for '{res['city']}']: {res['error']}")
            
    print("\n" + "=" * 50 + "\n")