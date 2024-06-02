# data/admin.py

"""
Admin configuration for the PowerConsumption model.

This script registers the PowerConsumption model with the Django admin site,
enabling it to be managed through the admin interface.

"""

from django.contrib import admin
from .models import PowerConsumption

admin.site.register(PowerConsumption)
