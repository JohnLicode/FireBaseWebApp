from django.contrib import admin
from django.urls import path

from fire.views import HomePageView, ChartView, PieCountbySeverity, LineCountbyMonth, MultilineIncidentTop3Country, multipleBarbySeverity, map_station, fire_incident_map
from fire.views import firestationListView, firestationCreateView, firestationUpdateView, firestationDeleteView
from fire.views import IncidentListView, IncidentCreateView, IncidentUpdateView, IncidentDeleteView
from fire.views import LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView
from fire.views import ConditionListView, ConditionCreateView, ConditionUpdateView, ConditionDeleteView
from fire.views import FiretruckListView, FiretruckCreateView, FiretruckUpdateView, FiretruckDeleteView
from fire.views import FirefightersListView, FirefightersCreateView, FirefightersUpdateView, FirefightersDeleteView


urlpatterns = [
    
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dashboard_chart', ChartView.as_view(), name='dashboard-chart'),
    path('chart/', PieCountbySeverity, name='chart'),
    path('lineChart/', LineCountbyMonth, name='chart'),
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('stations/', map_station, name='map-station'),  
    path('fire_incident_map/', fire_incident_map, name='fire-incidents-map'),
    
    path('firestation_list/', firestationListView.as_view(), name='station-list'),
    path('firestation_list/add', firestationCreateView.as_view(), name='firestation-add'),
    path('firestation_list/<pk>', firestationUpdateView.as_view(), name='firestation-update'),
    path('firestation_list/<pk>/delete/', firestationDeleteView.as_view(), name='firestation-delete'),

    path('incident_list/',  IncidentListView.as_view(), name='incident-list'),
    path('incident_list/add', IncidentCreateView.as_view(), name='incident-add'),
    path('incident_list/<pk>', IncidentUpdateView.as_view(), name='incident-update'),
    path('incident_list/<pk>/delete/', IncidentDeleteView.as_view(), name='incident-delete'),
    
    path('location_list/',  LocationListView.as_view(), name='loc-list'),
    path('location_list/add', LocationCreateView.as_view(), name='location-add'),
    path('location_list/<pk>', LocationUpdateView.as_view(), name='location-update'),
    path('location_list/<pk>/delete/', LocationDeleteView.as_view(), name='location-delete'),
    
    path('condition_list/',  ConditionListView.as_view(), name='weather-list'),
    path('condition_list/add', ConditionCreateView.as_view(), name='condition-add'),
    path('condition_list/<pk>', ConditionUpdateView.as_view(), name='condition-update'),
    path('condition_list/<pk>/delete/', ConditionDeleteView.as_view(), name='condition-delete'),
    
    
    path('firetruck_list/',  FiretruckListView.as_view(), name='fireTruck-list'),
    path('firetruck_list/add', FiretruckCreateView.as_view(), name='firetruck-add'),
    path('firetruck_list/<pk>', FiretruckUpdateView.as_view(), name='firetruck-update'),
    path('firetruck_list/<pk>/delete/', FiretruckDeleteView.as_view(), name='firetruck-delete'),
    
    path('firefighters/', FirefightersListView.as_view(), name='firefighters-list'),
    path('firefighters/add/', FirefightersCreateView.as_view(), name='firefighters-add'),
    path('firefighters/<int:pk>/edit/', FirefightersUpdateView.as_view(), name='firefighters-update'),  
    path('firefighters/<int:pk>/delete/', FirefightersDeleteView.as_view(), name='firefighters-delete'),


]
