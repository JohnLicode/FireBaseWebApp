from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from fire.models import Locations, Incident, FireStation, WeatherConditions, FireTruck, Firefighters
from fire.forms import Loc_Form, Incident_Form, FireStationzForm, Weather_condition, Firetruckform, FirefightersForm
from django.db.models.query import QuerySet
from django.db.models import Q


from django.views.generic.list import ListView
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth

from django.db.models import Count
from datetime import datetime


class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"
    
class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass


def PieCountbySeverity(request):
    query = '''
    SELECT severity_level, COUNT(*) as count
    FROM fire_incident
    GROUP BY severity_level
    '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    if rows:
        # Construct the dictionary with severity level as keys and count as values
        data = {severity: count for severity, count in rows}
    else:
        data = {}

    return JsonResponse(data)

def LineCountbyMonth(request):

    current_year = datetime.now().year

    result = {month: 0 for month in range(1, 13)}

    incidents_per_month = Incident.objects.filter(date_time__year=current_year) \
        .values_list('date_time', flat=True)

    # Counting the number of incidents per month
    for date_time in incidents_per_month:
        month = date_time.month
        result[month] += 1

    # If you want to convert month numbers to month names, you can use a dictionary mapping
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    result_with_month_names = {
        month_names[int(month)]: count for month, count in result.items()}

    return JsonResponse(result_with_month_names)

def MultilineIncidentTop3Country(request):

    query = '''
        SELECT 
        fl.country,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM 
        fire_incident fi
    JOIN 
        fire_locations fl ON fi.location_id = fl.id
    WHERE 
        fl.country IN (
            SELECT 
                fl_top.country
            FROM 
                fire_incident fi_top
            JOIN 
                fire_locations fl_top ON fi_top.location_id = fl_top.id
            WHERE 
                strftime('%Y', fi_top.date_time) = strftime('%Y', 'now')
            GROUP BY 
                fl_top.country
            ORDER BY 
                COUNT(fi_top.id) DESC
            LIMIT 3
        )
        AND strftime('%Y', fi.date_time) = strftime('%Y', 'now')
    GROUP BY 
        fl.country, month
    ORDER BY 
        fl.country, month;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Initialize a dictionary to store the result
    result = {}

    # Initialize a set of months from January to December
    months = set(str(i).zfill(2) for i in range(1, 13))

    # Loop through the query results
    for row in rows:
        country = row[0]
        month = row[1]
        total_incidents = row[2]

        # If the country is not in the result dictionary, initialize it with all months set to zero
        if country not in result:
            result[country] = {month: 0 for month in months}

        # Update the incident count for the corresponding month
        result[country][month] = total_incidents

    # Ensure there are always 3 countries in the result
    while len(result) < 3:
        # Placeholder name for missing countries
        missing_country = f"Country {len(result) + 1}"
        result[missing_country] = {month: 0 for month in months}

    for country in result:
        result[country] = dict(sorted(result[country].items()))

    return JsonResponse(result)

def multipleBarbySeverity(request):
    query = '''
    SELECT 
        fi.severity_level,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM 
        fire_incident fi
    GROUP BY fi.severity_level, month
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = {}
    months = set(str(i).zfill(2) for i in range(1, 13))

    for row in rows:
        level = str(row[0])  # Ensure the severity level is a string
        month = row[1]
        total_incidents = row[2]

        if level not in result:
            result[level] = {month: 0 for month in months}

        result[level][month] = total_incidents

    # Sort months within each severity level
    for level in result:
        result[level] = dict(sorted(result[level].items()))

    return JsonResponse(result)


def map_station(request):
     fireStations = FireStation.objects.values('name', 'latitude', 'longitude')

     for fs in fireStations:
         fs['latitude'] = float(fs['latitude'])
         fs['longitude'] = float(fs['longitude'])

     fireStations_list = list(fireStations)

     context = {
         'fireStations': fireStations_list,
     }

     return render(request, 'map_station.html', context)
 
def fire_incident_map(request):
    fireIncidents = Locations.objects.values('name', 'latitude', 'longitude')

    for fs in fireIncidents:
        fs['latitude'] = float(fs['latitude'])
        fs['longitude'] = float(fs['longitude'])

    fireIncidents_list = list(fireIncidents)  # Corrected variable name

    context = {
        'fireIncidents': fireIncidents_list,  # Corrected variable name
    }

    return render(request, 'fire_incident_map.html', context)

def firestation_list(request):
    firestations = FireStation.objects.all()
    return render(request, 'stationlist.html', {'object_list': firestations})



class firestationListView(ListView):
    model = FireStation
    template_name = 'station_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(country__icontains=query)
            )
        return qs
    
class firestationCreateView(CreateView):
    model = FireStation
    form_class = FireStationzForm
    template_name= 'station_add.html'
    success_url = reverse_lazy('station-list')
    
class firestationUpdateView(UpdateView):
    model = FireStation
    form_class = FireStationzForm
    template_name= 'station_edit.html'
    success_url = reverse_lazy('station-list')
    
class firestationDeleteView(DeleteView):
    model = FireStation
    template_name= 'station_del.html'
    success_url = reverse_lazy('station-list')
    


class IncidentListView(ListView):
    model = Incident
    template_name = 'incident_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(description__icontains=query) |
                Q(severity_level__icontains=query) |
                Q(location__name__icontains=query) |  # Assuming Locations model has a 'name' field
                Q(date_time__icontains=query)  # Assuming you want to search by date_time
            )
        return qs
    
class IncidentCreateView(CreateView):
    model = Incident
    form_class =  Incident_Form
    template_name= 'incident_add.html'
    success_url = reverse_lazy('incident-list')
    
class IncidentUpdateView(UpdateView):
    model = Incident
    form_class =  Incident_Form
    template_name= 'incident_edit.html'
    success_url = reverse_lazy('incident-list')
    
class IncidentDeleteView(DeleteView):
    model = Incident
    template_name= 'incident_del.html'
    success_url = reverse_lazy('incident-list')
    
class LocationListView(ListView):
    model = Locations
    template_name = 'loc_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(country__icontains=query)
            )
        return qs
    
class LocationCreateView(CreateView):
    model = Locations
    form_class = Loc_Form
    template_name= 'loc_add.html'
    success_url = reverse_lazy('loc-list')
    
class LocationUpdateView(UpdateView):
    model = Locations
    form_class = Loc_Form
    template_name= 'loc_edit.html'
    success_url = reverse_lazy('loc-list')
    
class LocationDeleteView(DeleteView):
    model = Locations
    template_name= 'loc_del.html'
    success_url = reverse_lazy('loc-list')

class ConditionListView(ListView):
    model = WeatherConditions
    context_object_name = 'object_list'
    template_name = 'weather_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ConditionListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(incident__location__name__icontains=query) | 
                Q(temperature__icontains=query) |
                Q(humidity__icontains=query) |
                Q(wind_speed__icontains=query) |
                Q(weather_description__icontains=query)
            )
        return qs
    
class ConditionCreateView(CreateView):
    model = WeatherConditions
    form_class = Weather_condition
    template_name = 'weather_add.html'
    success_url = reverse_lazy('weather-list')

class ConditionUpdateView(UpdateView):
    model = WeatherConditions
    form_class = Weather_condition
    template_name = 'weather_edit.html'
    success_url = reverse_lazy('weather-list')

class ConditionDeleteView(DeleteView):
    model = WeatherConditions
    template_name = 'weather_del.html'
    success_url = reverse_lazy('weather-list')
    
    
    
class FiretruckListView(ListView):
    model = FireTruck
    context_object_name = 'firetruck'
    template_name = 'firetruck_list.html'
    paginate_by = 10 
    
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(truck_number__icontains=query) | 
              Q(model__icontains=query) | 
              Q(capacity__icontains=query) | 
              Q(station__name__icontains=query))

        return qs

class FiretruckCreateView(CreateView):
    model = FireTruck
    form_class = Firetruckform
    template_name = 'firetruck_add.html'
    success_url = reverse_lazy('fireTruck-list')

class FiretruckUpdateView(UpdateView):
    model = FireTruck
    form_class = Firetruckform
    template_name = 'firetruck_edit.html'
    success_url = reverse_lazy('fireTruck-list')

class FiretruckDeleteView(DeleteView):
    model =  FireTruck
    template_name = 'firetruck_del.html'
    success_url = reverse_lazy('fireTruck-list')
    
    


class FirefightersListView(ListView):
    model = Firefighters
    context_object_name = 'firefighters'
    template_name = 'firefighter_list.html'
    paginate_by = 10 
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs

class FirefightersCreateView(CreateView):
    model = Firefighters
    form_class = FirefightersForm
    template_name = 'firefighter_add.html'
    success_url = reverse_lazy('firefighters-list')

class FirefightersUpdateView(UpdateView):
    model = Firefighters
    form_class = FirefightersForm
    template_name = 'firefighter_edit.html'
    success_url = reverse_lazy('firefighters-list')

class FirefightersDeleteView(DeleteView):
    model = Firefighters
    template_name = 'firefighter_del.html'
    success_url = reverse_lazy('firefighters-list')