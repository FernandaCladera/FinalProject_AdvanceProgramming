# App/views.py

"""_summary_
    Purpose: The views.py file contains the view functions that handle requests and return responses.
    Structure: It imports necessary modules and defines functions or classes that process requests and render templates or return data.
    Function: This lets the app respond to user actions, rendering web pages or providing data as needed.
"""

from django.shortcuts import render
from django.urls import reverse_lazy
from data.models import PowerConsumption
from .forms import trendForm
from django.http import JsonResponse
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
from datetime import datetime

#Home page view
def home(request):
    return render(request,'app/home.html')

#Home page after login
def index(request):
    return render(request,'app/index.html')

#Report view:
def report(request):
    return render(request,'app/report.html')

#Analysis view:
def analysis(request):
    return render(request,'app/analysis.html')

#View of the data
def power_consumption_list(request):
    data=PowerConsumption.objects.all()
    return render(request, 'app/data.html',{'data':data}) 

## CREATE PLOTLY GRAPH
def dashboard(request):
    # Fetch the first and last dates from the data
    data_all = PowerConsumption.objects.all()
    if data_all.exists():
        default_start = data_all.earliest('date').date
        default_end = data_all.latest('date').date
    else:
        default_start = datetime.today().date()
        default_end = datetime.today().date()

    # First Trend Graph: Variables
    form = trendForm(request.GET)
    chart1 = None
    zone_charts = {}
    histogram_charts = {}

    # Set default variable if none is provided
    default_variable = 'temperature'

    # If the form is valid, get the dates and variable from the form, otherwise use defaults
    if form.is_valid():
        start = form.cleaned_data.get('start') or default_start
        end = form.cleaned_data.get('end') or default_end
        variable = form.cleaned_data.get('variable') or default_variable
    else:
        start = default_start
        end = default_end
        variable = default_variable

    data = PowerConsumption.objects.all()
    if start:
        data = data.filter(date__gte=start)
    if end:
        data = data.filter(date__lte=end)

    # Generate the main variable trend graph
    if variable:
        fig1 = px.line(
            x=[c.date for c in data],
            y=[getattr(c, variable) for c in data],
            title=f"{variable.replace('_', ' ').title()} Over Time",
            labels={'x': 'Date', 'y': variable.replace('_', ' ').title()}
        )
        fig1.update_layout(title={
            'font_size': 22,
            'x': 0.5
        },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,1)')
        chart1 = fig1.to_html()

    # Generate graphs for each zone
    zones = ['zone_1_power_consumption', 'zone_2_power_consumption', 'zone_3_power_consumption']
    for zone in zones:
        fig = px.line(
            x=[c.date for c in data],
            y=[getattr(c, zone) for c in data],
            title=f"{zone.replace('_', ' ').title()} Over Time",
            labels={'x': 'Date', 'y': zone.replace('_', ' ').title()}
        )
        fig.update_layout(title={
            'font_size': 22,
            'x': 0.5
        },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,1)'
            )
        zone_charts[zone] = fig.to_html()

        # Generate Histogram for each zone
        zone_data = [getattr(c, zone) for c in data]
        fig_hist = go.Figure(data=[go.Histogram(
            x=zone_data,
            nbinsx=30,
            marker_color='blue',
            marker_line_color='black',
            marker_line_width=1.2
        )])
        fig_hist.update_layout(
            title=f'{zone.replace("_", " ").title()}',
            yaxis_title='Frequency',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,1)',
        )
        histogram_charts[zone] = fig_hist.to_html()

    context = {
        'chart1': chart1,
        'form': form,
        'zone_charts': zone_charts,
        'histogram_charts': histogram_charts,
        'default_start': default_start,
        'default_end': default_end,
        'default_variable': default_variable
    }
    return render(request, 'app/dashboard.html', context)
