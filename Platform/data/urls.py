# data/urls.py

"""_summary_
This module defines the URL patterns for the 'data' application, routing requests to the appropriate view functions.

Functions:
    power_consumption_data - A view function that provides power consumption data in JSON format.

"""

from django.urls import path
from .views import power_consumption_data

urlpatterns = [
    path('power_consumption_data/',power_consumption_data,name='power_consumption_data'),
]
