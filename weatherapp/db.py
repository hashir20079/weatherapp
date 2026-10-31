import sqlite3

def init_db():
    """
    Creates an in-memory SQLite database connection and sets up the table.
    """
    conn = sqlite3.connect(':memory:')  # Data exists ONLY in RAM
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            country TEXT,
            temp REAL,
            feels_like REAL,
            humidity INTEGER,
            wind_speed REAL,
            description TEXT,
            sunrise TEXT,
            sunset TEXT
        )
    ''')
    conn.commit()
    return conn

def store_weather_data(conn, results):
    """
    Stores successfully fetched weather records into the in-memory database.
    """
    cursor = conn.cursor()
    for res in results:
        if res.get("success"):
            cursor.execute('''
                INSERT INTO weather_records (city, country, temp, feels_like, humidity, wind_speed, description, sunrise, sunset)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                res["city"],
                res["country"],
                res["temp"],
                res["feels_like"],
                res["humidity"],
                res["wind_speed"],
                res["description"],
                res["sunrise"],
                res["sunset"]
            ))
    conn.commit()

def fetch_all_weather_records(conn):
    """
    Retrieves stored records from the in-memory database including sunrise and sunset.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT city, temp, humidity, wind_speed, description, sunrise, sunset FROM weather_records")
    return cursor.fetchall()