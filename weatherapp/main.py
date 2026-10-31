# main.py

import sys
from input import get_api_key, get_city_inputs
from api import fetch_weather_data
from display import display_weather_data
from db import init_db, store_weather_data
from visualize import plot_weather_data

def main():
    print("--- Python Modular Weather CLI with In-Memory DB ---")
    
    # 1. Initialize In-Memory SQLite Database (wiped when script exits)
    db_conn = init_db()

    # 2. Take API key as runtime input
    api_key = get_api_key()
    if not api_key:
        print("⚠️ API key cannot be empty. Exiting.")
        sys.exit(1)
        
    while True:
        # 3. Get validated city inputs (1-3 cities)
        cities = get_city_inputs()
        
        # 4. Fetch data from the API
        print("Fetching weather data...")
        weather_results = fetch_weather_data(cities, api_key)
        
        # 5. Store fetched results in the temporary SQLite database
        store_weather_data(db_conn, weather_results)
        
        # 6. Display terminal output
        display_weather_data(weather_results)
        
        # 7. Ask to visualize data
        show_chart = input("Do you want to visualize this data in graphics? (y/n): ").strip().lower()
        if show_chart in ['y', 'yes']:
            plot_weather_data(db_conn)
        
        # Prompt to run again or exit
        choice = input("Do you want to check another set of cities? (y/n): ").strip().lower()
        if choice not in ['y', 'yes']:
            print("Closing application. In-memory database has been cleared.")
            db_conn.close()
            sys.exit(0)

if __name__ == "__main__":
    main()