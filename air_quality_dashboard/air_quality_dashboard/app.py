from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Use your actual API key
api_key = "3e63907ee622fce9a0d20f0298881f07"

# Load the trained model
model = joblib.load('air_quality_model.pkl')

# Function to get latitude and longitude for the given city
def get_coordinates(city):
    geo_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

@app.route('/air_quality')
def air_quality():
    city = request.args.get('city', 'Delhi')
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return jsonify({"error": "City not found"}), 404
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        components = data['list'][0]['components']
        return jsonify(components)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching air quality data: {e}")
        return jsonify({"error": "Failed to fetch air quality data"}), 500

@app.route('/predict_air_quality')
def predict_air_quality():
    try:
        co = float(request.args.get('co'))
        no = float(request.args.get('no'))
        no2 = float(request.args.get('no2'))
        o3 = float(request.args.get('o3'))
        so2 = float(request.args.get('so2'))
        pm2_5 = float(request.args.get('pm2_5'))
        pm10 = float(request.args.get('pm10'))
        nh3 = float(request.args.get('nh3'))

        # Prepare features for prediction
        features = np.array([[co, no, no2, o3, so2, pm2_5, pm10, nh3]])
        
        # Predict using the model
        prediction = model.predict(features)
        
        return jsonify({'predicted_air_quality': prediction[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
