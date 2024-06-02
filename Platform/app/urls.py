# app/urls.py

"""_summary_
    Purpose: The urls.py file maps URL paths to view functions in the app.
    Structure: It imports needed modules and defines urlpatterns, where each path() links a URL to a view.
    Function: This lets the app handle different URLs and direct requests to the right views for the correct response.
"""

from django.urls import path
from . import views

app_name='app'

urlpatterns = [
    path("",views.home,name="home"),
    path('home/',views.home, name='home'),
    path('index/',views.index,name="index"),
    path('report/',views.report,name="report"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('analysis/',views.analysis,name="analysis"),
]
