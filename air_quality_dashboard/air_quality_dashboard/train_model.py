import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

def calculate_aqi(concentration, breakpoints):
    for i in range(len(breakpoints) - 1):
        if breakpoints[i][0] <= concentration <= breakpoints[i + 1][0]:
            Clow, Chigh = breakpoints[i][0], breakpoints[i + 1][0]
            Ilow, Ihigh = breakpoints[i][1], breakpoints[i + 1][1]
            aqi = ((Ihigh - Ilow) / (Chigh - Clow)) * (concentration - Clow) + Ilow
            return round(aqi)
    return None

# Define breakpoints for pollutants
pm25_breakpoints = [
    (0.0, 0), (12.0, 50), (35.4, 100), (55.4, 150),
    (150.4, 200), (250.4, 300), (350.4, 400), (500.4, 500)
]

pm10_breakpoints = [
    (0.0, 0), (54, 50), (154, 100), (254, 150),
    (354, 200), (424, 300), (504, 400), (604, 500)
]

co_breakpoints = [
    (0.0, 0), (4.4, 50), (9.4, 100), (12.4, 150),
    (15.4, 200), (30.4, 300), (40.4, 400), (50.4, 500)
]

no2_breakpoints = [
    (0.0, 0), (53, 50), (100, 100), (360, 150),
    (649, 200), (1249, 300), (1649, 400), (2049, 500)
]

o3_breakpoints = [
    (0.0, 0), (54, 50), (70, 100), (85, 150),
    (105, 200), (200, 300), (300, 400), (400, 500)
]

so2_breakpoints = [
    (0.0, 0), (35, 50), (75, 100), (185, 150),
    (304, 200), (604, 300), (804, 400), (1004, 500)
]

nh3_breakpoints = [
    (0.0, 0), (0.2, 50), (0.4, 100), (0.6, 150),
    (0.8, 200), (1.0, 300), (1.2, 400), (1.4, 500)
]

no_breakpoints = [
    (0.0, 0), (0.05, 50), (0.1, 100), (0.2, 150),
    (0.4, 200), (0.8, 300), (1.0, 400), (1.2, 500)
]

print("Loading data...")
# Load your historical air quality data
data = pd.read_csv('air_quality_data.csv')

# Ensure the data follows the specified order
columns_order = ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3', 'timestamp']
data = data[columns_order]

print("Calculating AQI for each pollutant...")
# Calculate AQI for each pollutant
data['PM2.5_AQI'] = data['pm2_5'].apply(lambda x: calculate_aqi(x, pm25_breakpoints))
data['PM10_AQI'] = data['pm10'].apply(lambda x: calculate_aqi(x, pm10_breakpoints))
data['CO_AQI'] = data['co'].apply(lambda x: calculate_aqi(x, co_breakpoints))
data['NO2_AQI'] = data['no2'].apply(lambda x: calculate_aqi(x, no2_breakpoints))
data['O3_AQI'] = data['o3'].apply(lambda x: calculate_aqi(x, o3_breakpoints))
data['SO2_AQI'] = data['so2'].apply(lambda x: calculate_aqi(x, so2_breakpoints))
data['NH3_AQI'] = data['nh3'].apply(lambda x: calculate_aqi(x, nh3_breakpoints))
data['NO_AQI'] = data['no'].apply(lambda x: calculate_aqi(x, no_breakpoints))

print("Preparing data for training...")
# Prepare the data in the specified order
X = data[['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']]  # Feature columns
y = data[['CO_AQI', 'NO_AQI', 'NO2_AQI', 'O3_AQI', 'SO2_AQI', 'PM2.5_AQI', 'PM10_AQI', 'NH3_AQI']].mean(axis=1)  # Average AQI as the target

print("Splitting data into training and test sets...")
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the model...")
# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

print("Model trained successfully.")
print("Saving the model to air_quality_model.pkl...")
# Save the model
joblib.dump(model, 'air_quality_model.pkl')

print("Model saved successfully.")
