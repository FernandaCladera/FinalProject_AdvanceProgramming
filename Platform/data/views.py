# data/views.py

"""_summary_
This module defines the view for retrieving power consumption data and providing it as a JSON response (API Endpoint).

Functions:
    power_consumption_data - Retrieves power consumption data from the database and returns it in JSON format.
"""

from django.shortcuts import render
from django.http import JsonResponse
from .models import PowerConsumption

def power_consumption_data(request):
    data=PowerConsumption.objects.all().values(
        'date','temperature','humidity','wind_speed',
        'general_diffuse_flows','diffuse_flows',
        'zone_1_power_consumption', 'zone_2_power_consumption', 
        'zone_3_power_consumption'        
    )
    return JsonResponse(list(data),safe=False)

