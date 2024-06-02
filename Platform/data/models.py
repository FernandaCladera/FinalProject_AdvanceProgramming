# data/models.py

from django.db import models
from django.contrib.auth.models import User

"""
The PowerConsumption model represents power consumption data along with related features for forecasting.

Attributes:
    Various fields to store data related to date, temperature, humidity, wind speed, general diffuse flows,
    and power consumption for different zones, as well as engineered features for forecasting.

Methods:
    __str__(): Returns a string representation of the instance, showing the date and power consumption values
               for Zone 1, Zone 2, and Zone 3.
"""


class PowerConsumption(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    general_diffuse_flows = models.FloatField()
    diffuse_flows = models.FloatField()
    zone_1_power_consumption = models.FloatField()
    zone_2_power_consumption = models.FloatField()
    zone_3_power_consumption = models.FloatField()
    
    # Engineered Features for forecasting
    # Time features
    hour = models.IntegerField(null=True, blank=True)
    dayofweek = models.IntegerField(null=True, blank=True)
    quarter = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    dayofyear = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    is_weekend = models.BooleanField(default=False)
    
    # Statistic features
    zone_1_power_consumption_lag_1=models.FloatField(null=True,blank=True)
    zone_1_power_consumption_lag_2=models.FloatField(null=True,blank=True)
    zone_1_power_consumption_rolling_mean_3=models.FloatField(null=True,blank=True)
    zone_1_power_consumption_rolling_std_3=models.FloatField(null=True,blank=True)
    zone_1_power_consumption_ema_3=models.FloatField(null=True,blank=True)
    
    zone_2_power_consumption_lag_1=models.FloatField(null=True,blank=True)
    zone_2_power_consumption_lag_2=models.FloatField(null=True,blank=True)
    zone_2_power_consumption_rolling_mean_3=models.FloatField(null=True,blank=True)
    zone_2_power_consumption_rolling_std_3=models.FloatField(null=True,blank=True)
    zone_2_power_consumption_ema_3=models.FloatField(null=True,blank=True)
    
    zone_3_power_consumption_lag_1=models.FloatField(null=True,blank=True)
    zone_3_power_consumption_lag_2=models.FloatField(null=True,blank=True)
    zone_3_power_consumption_rolling_mean_3=models.FloatField(null=True,blank=True)
    zone_3_power_consumption_rolling_std_3=models.FloatField(null=True,blank=True)
    zone_3_power_consumption_ema_3=models.FloatField(null=True,blank=True)
    
    def __str__(self):
        return (f"{self.date}-"
                f"Zone 1:{self.zone_1_power_consumption} kW,"
                f"Zone 2:{self.zone_2_power_consumption} kW,"
                f"Zone 3: {self.zone_3_power_consumption} kW")