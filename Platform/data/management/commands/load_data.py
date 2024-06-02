# management/commands / load_data.py
"""
This module provides a custom Django management command for loading power consumption data from a CSV file into the database.
Functions:
    handle - Executes the data loading process from the specified CSV file.
Classes:
    Command - A custom management command for loading power consumption data.
"""

import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from data.models import PowerConsumption


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        file_path= os.path.join(settings.BASE_DIR, 'static', 'data', 'Tetuan_City_power_consumption.csv')
        try:
            # File handling part
            with open(file_path,'r') as file:
                reader=csv.DictReader(file)
                # Data processing part
                for row in reader:
                    PowerConsumption.objects.create(
                        date=datetime.strptime(row['DateTime'],'%m/%d/%Y %H:%M'),
                        temperature=float(row['Temperature']),
                        humidity=float(row['Humidity']),
                        wind_speed=float(row['Wind Speed']),
                        general_diffuse_flows=float(row['general diffuse flows']),
                        diffuse_flows=float(row['diffuse flows']),
                        zone_1_power_consumption=float(row['Zone 1 Power Consumption']),
                        zone_2_power_consumption=float(row['Zone 2  Power Consumption']),
                        zone_3_power_consumption=float(row['Zone 3  Power Consumption']),
                    )
            # Confirmation messages
            self.stdout.write(self.style.SUCCESS('Data successfully loaded'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
    