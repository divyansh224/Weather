import requests
import pandas as pd
from datetime import datetime, timedelta

api_key = "3e63907ee622fce9a0d20f0298881f07"
base_url = "http://api.openweathermap.org/data/2.5/air_pollution/history"

# Function to fetch historical data for a city
def fetch_historical_data(city, start_date, end_date):
    geo_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(geo_url)
    data = response.json()
    lat = data['coord']['lat']
    lon = data['coord']['lon']

    # Fetch historical data
    params = {
        'lat': lat,
        'lon': lon,
        'start': int(start_date.timestamp()),
        'end': int(end_date.timestamp()),
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data['list']

# Function to save data to CSV
def save_data_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Example usage
city = "Delhi"
start_date = datetime.now() - timedelta(days=30)  # Last 30 days
end_date = datetime.now()
data = fetch_historical_data(city, start_date, end_date)

# Processing data to a suitable format
processed_data = []
for entry in data:
    timestamp = datetime.utcfromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S')
    components = entry['components']
    components['timestamp'] = timestamp
    processed_data.append(components)

save_data_to_csv(processed_data, 'air_quality_data.csv')
