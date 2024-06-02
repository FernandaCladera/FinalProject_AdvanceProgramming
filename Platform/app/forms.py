# App/forms.py

"""
Form to modify the dates and select a variable in our dashboard view.

This form captures a start date, an end date, and a variable from predefined choices.

"""

from django import forms

#Form to modify the dates in our dashboard view:

class trendForm(forms.Form):
    start=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    variable=forms.ChoiceField(
        choices=[
            ('temperature','Temperature'),
            ('humidity','Humidity'),
            ('wind_speed','Wind Speed'),
            ('general_diffuse_flows','General Diffuse Flows'),
            ('diffuse_flows','Diffuse Flows')
            ],
        widget=forms.Select(attrs={'class':'form-control'}),
        required=True
    )