# data/management/commands/cleaning_data.py

"""
This module provides a custom Django management command for cleaning and preprocessing the power consumption dataset.

Functions:
    handle - Executes the data cleaning and preprocessing steps.

Classes:
    Command - A custom management command for data cleaning and preprocessing.

"""

import pandas as pd
from django.core.management.base import BaseCommand
from data.models import PowerConsumption
from sklearn.preprocessing import MinMaxScaler

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        def load_data():
            data=list(PowerConsumption.objects.all().values())
            df=pd.DataFrame(data)
            return df
        
        def handle_missing_values(df):
            for column in df.columns:
                if df[column].dtype != 'object' and column !='date':
                    df[column].fillna(df[column].mean(),inplace=True)
            return df
        
        def normalize_features(df):
            scaler=MinMaxScaler()
            features_to_scale=['temperature','humidity','wind_speed','general_diffuse_flows','diffuse_flows']
            
            df[features_to_scale]=scaler.fit_transform(df[features_to_scale])
            return df
        
        def create_features(df):
            df=df.copy()
            df['hour']=pd.to_datetime(df['date']).dt.hour
            df['dayofweek']=pd.to_datetime(df['date']).dt.dayofweek
            df['quarter']=pd.to_datetime(df['date']).dt.quarter
            df['month']=pd.to_datetime(df['date']).dt.month
            df['year']=pd.to_datetime(df['date']).dt.year
            df['dayofyear']=pd.to_datetime(df['date']).dt.dayofyear
            df['day']=pd.to_datetime(df['date']).dt.day
            df['is_weekend']=pd.to_datetime(df['date']).dt.dayofweek>=5
            
            target=['zone_1_power_consumption', 'zone_2_power_consumption', 'zone_3_power_consumption']
            
            for zone in target:
                df[f'{zone}_lag_1']=df[zone].shift(1)
                df[f'{zone}_lag_2']=df[zone].shift(2)
                df[f'{zone}_rolling_mean_3']=df[zone].rolling(window=3).mean()
                df[f'{zone}_rolling_std_3']=df[zone].rolling(window=3).std()
                df[f'{zone}_ema_3']=df[zone].ewm(span=3,adjust=False).mean()
            return df
        
        def preprocess_data():
            df=load_data()
            self.stdout.write(self.style.SUCCESS("Data loaded"))
            
            df=handle_missing_values(df)
            self.stdout.write(self.style.SUCCESS("Missing values handled"))
            
            df=normalize_features(df)
            self.stdout.write(self.style.SUCCESS("Additional features created"))
            
            return df
        
        def save_cleaned_data_to_db(df):
            for index, row in df.iterrows():
                PowerConsumption.objects.filter(id=row['id']).update(
                    temperature=row['temperature'],
                    humidity=row['humidity'],
                    wind_speed=row['wind_speed'],
                    general_diffuse_flows=row['general_diffuse_flows'],
                    diffuse_flows=row['diffuse_flows'],
                    zone_1_power_consumption=row['zone_1_power_consumption'],
                    zone_2_power_consumption=row['zone_2_power_consumption'],
                    zone_3_power_consumption=row['zone_3_power_consumption'],
                    hour=row['hour'],
                    dayofweek=row['dayofweek'],
                    quarter=row['quarter'],
                    month=row['month'],
                    year=row['year'],
                    dayofyear=row['dayofyear'],
                    day=row['day'],
                    is_weekend=row['is_weekend'],
                    zone_1_power_consumption_lag_1=row['zone_1_power_consumption_lag_1'],
                    zone_1_power_consumption_lag_2=row['zone_1_power_consumption_lag_2'],
                    zone_1_power_consumption_rolling_mean_3=row['zone_1_power_consumption_rolling_mean_3'],
                    zone_1_power_consumption_rolling_std_3=row['zone_1_power_consumption_rolling_std_3'],
                    zone_1_power_consumption_ema_3=row['zone_1_power_consumption_ema_3'],
                    zone_2_power_consumption_lag_1=row['zone_2_power_consumption_lag_1'],
                    zone_2_power_consumption_lag_2=row['zone_2_power_consumption_lag_2'],
                    zone_2_power_consumption_rolling_mean_3=row['zone_2_power_consumption_rolling_mean_3'],
                    zone_2_power_consumption_rolling_std_3=row['zone_2_power_consumption_rolling_std_3'],
                    zone_2_power_consumption_ema_3=row['zone_2_power_consumption_ema_3'],
                    zone_3_power_consumption_lag_1=row['zone_3_power_consumption_lag_1'],
                    zone_3_power_consumption_lag_2=row['zone_3_power_consumption_lag_2'],
                    zone_3_power_consumption_rolling_mean_3=row['zone_3_power_consumption_rolling_mean_3'],
                    zone_3_power_consumption_rolling_std_3=row['zone_3_power_consumption_rolling_std_3'],
                    zone_3_power_consumption_ema_3=row['zone_3_power_consumption_ema_3'],
                )
            self.stdout.write(self.style.SUCCESS("Cleaned data saved to database"))                
            
        cleaned_data = preprocess_data()
        save_cleaned_data_to_db(cleaned_data)
        self.stdout.write(self.style.SUCCESS("Data cleaning process completed :)"))            
            
        
        