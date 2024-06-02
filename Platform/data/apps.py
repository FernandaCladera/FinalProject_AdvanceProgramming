# data/apps.py

"""
Configuration for the Data app.

This script defines the configuration for the Data app within the Django project.

"""

from django.apps import AppConfig


class DataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data'
