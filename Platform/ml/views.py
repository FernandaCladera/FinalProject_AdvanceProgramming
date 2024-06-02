# ml/views.py

"""_summary_

his module defines the view for generating monthly energy consumption forecasts using a pre-trained XGBoost model. 
It includes functions for handling data retrieval, feature creation, and prediction.

Functions:
    forecast_next_month - Generates and returns monthly energy consumption forecasts based on historical data.

"""

import pandas as pd
import joblib
from django.shortcuts import render
from django.http import JsonResponse
from data.models import PowerConsumption

model = joblib.load('/Users/fernandacladeramelgar/Documents/Projects/ADA_AP_FinalProject/ADA_FP/best_xgb_model.pkl')

features = [
    'temperature', 'humidity', 'wind_speed', 'general_diffuse_flows',
    'diffuse_flows', 'hour', 'dayofweek', 'quarter', 'month',
    'year', 'dayofyear', 'day', 'is_weekend',
    'zone_1_power_consumption_lag_1', 'zone_1_power_consumption_lag_2',
    'zone_1_power_consumption_rolling_mean_3', 'zone_1_power_consumption_rolling_std_3',
    'zone_1_power_consumption_ema_3',
    'zone_2_power_consumption_lag_1', 'zone_2_power_consumption_lag_2',
    'zone_2_power_consumption_rolling_mean_3', 'zone_2_power_consumption_rolling_std_3',
    'zone_2_power_consumption_ema_3',
    'zone_3_power_consumption_lag_1', 'zone_3_power_consumption_lag_2',
    'zone_3_power_consumption_rolling_mean_3', 'zone_3_power_consumption_rolling_std_3',
    'zone_3_power_consumption_ema_3'
]

def forecast_next_month(request):
    start_date = '2018-01-01'
    end_date = '2018-01-31'
    
    historical_data = PowerConsumption.objects.filter(date__lt=start_date).order_by('-date')[:60]  
    if not historical_data.exists():
        return JsonResponse({'error': 'No historical data available for feature creation'}, status=400)
    
    historical_df = pd.DataFrame.from_records(historical_data.values())
    historical_df = historical_df.sort_values(by='date')  
    
    future_dates = pd.date_range(start=start_date, end=end_date)
    
    forecast_df = pd.DataFrame(index=future_dates, columns=features)
    
    for feature in features:
        if feature in historical_df.columns:
            forecast_df[feature] = historical_df[feature].iloc[-1]
    
    forecast_df['date'] = forecast_df.index
    forecast_df['hour'] = forecast_df['date'].dt.hour
    forecast_df['dayofweek'] = forecast_df['date'].dt.dayofweek
    forecast_df['quarter'] = forecast_df['date'].dt.quarter
    forecast_df['month'] = forecast_df['date'].dt.month
    forecast_df['year'] = forecast_df['date'].dt.year
    forecast_df['dayofyear'] = forecast_df['date'].dt.dayofyear
    forecast_df['day'] = forecast_df['date'].dt.day
    forecast_df['is_weekend'] = forecast_df['date'].dt.dayofweek >= 5
    
    for zone in ['zone_1_power_consumption', 'zone_2_power_consumption', 'zone_3_power_consumption']:
        forecast_df[f'{zone}_lag_1'] = historical_df[zone].shift(1).iloc[-1]
        forecast_df[f'{zone}_lag_2'] = historical_df[zone].shift(2).iloc[-1]
        forecast_df[f'{zone}_rolling_mean_3'] = historical_df[zone].rolling(window=3).mean().iloc[-1]
        forecast_df[f'{zone}_rolling_std_3'] = historical_df[zone].rolling(window=3).std().iloc[-1]
        forecast_df[f'{zone}_ema_3'] = historical_df[zone].ewm(span=3, adjust=False).mean().iloc[-1]
    
    # Fill NaN values that might result from shift and rolling operations
    forecast_df.fillna(method='bfill', inplace=True)
    forecast_df.fillna(method='ffill', inplace=True)
    
    X_forecast = forecast_df[features]
    predictions = model.predict(X_forecast)
    
    results = []
    for i, date in enumerate(future_dates):
        results.append({
            'date': date.strftime('%Y-%m-%d'),
            'zone_1_power_consumption': predictions[i][0] if predictions.ndim > 1 else predictions[i],
            'zone_2_power_consumption': predictions[i][1] if predictions.ndim > 1 else predictions[i],
            'zone_3_power_consumption': predictions[i][2] if predictions.ndim > 1 else predictions[i],
        })
    
    return render(request, 'ml/forecast.html', {'predictions': results})
