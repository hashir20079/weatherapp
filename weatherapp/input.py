# inputs.py

def get_api_key():
    """
    Prompts the user to enter their OpenWeatherMap API key at runtime.
    """
    key = input("Enter your OpenWeatherMap API key: ").strip()
    return key

def get_city_inputs():
    """
    Prompts the user for city inputs.
    Enforces a minimum of 1 city and a maximum of 3 cities.
    Returns a list of valid city names.
    """
    while True:
        raw_input = input("Enter 1 to 3 cities (comma-separated, e.g., Karachi, London, Tokyo): ").strip()
        if not raw_input:
            print("⚠️ Input cannot be empty. Please try again.")
            continue
            
        cities = [city.strip() for city in raw_input.split(",") if city.strip()]
        
        if len(cities) < 1:
            print("⚠️ Please enter at least 1 city.")
        elif len(cities) > 3:
            print(f"⚠️ You entered {len(cities)} cities. Maximum allowed is 3. Please try again.")
        else:
            return cities