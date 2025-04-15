from django.forms import ModelForm
from django import forms
from .models import Locations, Incident, FireStation, WeatherConditions, FireTruck, Firefighters

class Loc_Form(ModelForm):
    class Meta:
        model = Locations
        fields = "__all__"

class Incident_Form(ModelForm):
    date_time = forms.DateTimeField(
        label="Incident Date & Time",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )

    class Meta:
        model = Incident
        fields = "__all__"

class FireStationzForm(ModelForm):
    class Meta:
        model = FireStation
        fields = "__all__"

class Weather_condition(ModelForm):
    class Meta:
        model = WeatherConditions
        fields = "__all__"
        
        
class Firetruckform(ModelForm):
    class Meta: 
        model = FireTruck
        fields = "__all__" 
        
class FirefightersForm(forms.ModelForm):
    class Meta:
        model = Firefighters
        fields = "__all__" 
