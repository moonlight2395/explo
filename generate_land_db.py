import sqlite3
import random
import os
from datetime import datetime, timedelta

def create_land_db():
    db_name = 'ap_transit_land.db'
    
    # Remove old DB if it exists to prevent overlap issues
    if os.path.exists(db_name):
        os.remove(db_name)
        
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table matching your dashboard schema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transit_data (
        name TEXT, lat REAL, lon REAL, delay REAL,
        perf TEXT, hour INTEGER, sched TEXT, actual TEXT
    )
    ''')

    # Exact land coordinates for AP & Telangana cities
    city_anchors = {
        "Visakhapatnam": (17.6868, 83.2185),
        "Vijayawada": (16.5062, 80.6480),
        "Tirupati": (13.6288, 79.4192),
        "Guntur": (16.3067, 80.4365),
        "Nellore": (14.4426, 79.9865),
        "Kurnool": (15.8281, 78.0373),
        "Rajahmundry": (17.0005, 81.8040),
        "Kakinada": (16.9891, 82.2475),
        "Kadapa": (14.4673, 78.8242),
        "Anantapur": (14.6819, 77.6006),
        "Ongole": (15.5057, 80.0499),
        "Eluru": (16.7107, 81.1031),
        "Machilipatnam": (16.1786, 81.1332),
        "Vizianagaram": (18.1067, 83.3956),
        "Srikakulam": (18.3000, 83.8966),
        "Warangal": (17.9689, 79.5941),
        "Nizamabad": (18.6705, 78.1000),
        "Karimnagar": (18.4386, 79.1288),
        "Khammam": (17.2473, 80.1514),
        "Mahbubnagar": (16.7431, 78.0069),
        "Nalgonda": (17.0500, 79.2700),
        "Adilabad": (19.6766, 78.5342),
        "Medak": (18.0460, 78.2618),
        "Sangareddy": (17.6163, 78.0827),
        "Proddatur": (14.7397, 78.5529),
        "Hindupur": (13.8291, 77.4947),
        "Chittoor": (13.2172, 79.1003),
        "Bhimavaram": (16.5441, 81.5212),
        "Narasaraopet": (16.2360, 80.0503),
        "Hyderabad": (17.3850, 78.4867)
    }

    data_rows = []
    base_date = datetime(2024, 10, 1)

    # Generate 10 stops per city = 300 total stations
    for city, (base_lat, base_lon) in city_anchors.items():
        for i in range(1, 11): 
            stop_name = f"{city} Stop {i}"
            
            # Apply a tiny random offset (approx 0 to 5 kilometers max) to cluster stops around the city
            lat = round(base_lat + random.uniform(-0.04, 0.04), 4)
            lon = round(base_lon + random.uniform(-0.04, 0.04), 4)
            
            # Random delay between -10 mins (early) and 30 mins (late)
            delay = round(random.uniform(-10.0, 30.0), 2)
            
            # Categorize
            if delay <= 2:
                perf = "On-Time"
            elif delay <= 8:
                perf = "Slightly Late"
            else:
                perf = "Heavy Delay"
                
            hour = random.randint(0, 23)
            
            # Time formatting
            sched_time = base_date + timedelta(days=random.randint(0, 7), hours=hour, minutes=random.randint(0, 59))
            actual_time = sched_time + timedelta(minutes=delay)
            
            sched_str = sched_time.strftime("%Y-%m-%d %H:%M:00")
            actual_str = actual_time.strftime("%Y-%m-%d %H:%M:%S")
            
            data_rows.append((stop_name, lat, lon, delay, perf, hour, sched_str, actual_str))

    cursor.executemany('''
    INSERT INTO transit_data (name, lat, lon, delay, perf, hour, sched, actual)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data_rows)

    conn.commit()
    conn.close()
    print(f"Successfully generated {len(data_rows)} land-based stations in {db_name}")

if __name__ == "__main__":
    create_land_db()
