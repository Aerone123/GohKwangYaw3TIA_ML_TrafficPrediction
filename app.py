from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)

model_path = 'xgboost_model.pkl'
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.json
        
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        wind_speed = float(data['wind_speed'])
        clouds_all = float(data['clouds_all'])
        
        dt_str = data['datetime']
        dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
        
        hour = dt.hour
        day_of_week = dt.weekday()
        month = dt.month
        year = dt.year
        is_weekend = 1 if day_of_week >= 5 else 0
        
        weather_type = data['weather_type']
        weather_features = {
            'weather_type_Clouds': 0, 'weather_type_Drizzle': 0, 'weather_type_Fog': 0,
            'weather_type_Haze': 0, 'weather_type_Mist': 0, 'weather_type_Rain': 0,
            'weather_type_Smoke': 0, 'weather_type_Snow': 0, 'weather_type_Squall': 0,
            'weather_type_Thunderstorm': 0
        }
        
        key = f"weather_type_{weather_type}"
        if key in weather_features:
            weather_features[key] = 1
            
        input_data = pd.DataFrame([{
            'humidity': humidity,
            'wind_speed': wind_speed,
            'temperature': temperature,
            'clouds_all': clouds_all,
            'hour': hour,
            'day_of_week': day_of_week,
            'month': month,
            'year': year,
            'is_weekend': is_weekend,
            **weather_features
        }])
        
        prediction = model.predict(input_data)[0]
        
        return jsonify({'prediction': float(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
