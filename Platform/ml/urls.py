# ml/urls.py

"""_summary_

This module defines the URL patterns for the 'ml' application, routing requests to the appropriate view functions.

Functions:
    forecast_next_month - A view function that generates monthly predictions based on historical data.
"""

from django.urls import path
from .views import forecast_next_month

app_name = 'ml'

urlpatterns = [
    path('forecast/', forecast_next_month, name='forecast_next_month'),
]