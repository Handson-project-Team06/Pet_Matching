from matching.models import Pet, GENDER_CHOICES, ANIMAL_CHOICES
import django_filters
from django_filters import FilterSet, CharFilter, ChoiceFilter
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy
from django.db.models.expressions import RawSQL
import math
from django.db.backends.signals import connection_created
from django.dispatch import receiver
from math import radians, cos, sin, asin, sqrt
import urllib.request,urllib.parse
import json


class PetFilter(FilterSet):
    breed = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.ChoiceFilter(choices=GENDER_CHOICES,empty_label=ugettext_lazy(u'Any'))
    animal = django_filters.ChoiceFilter(choices=ANIMAL_CHOICES,empty_label=ugettext_lazy(u'Any'))
    class Meta:
        model = Pet
        fields = ['animal', 'gender','breed']



def getplace(lat, lon):
    key = "AIzaSyBlu5QpKaxho5vC2yN871kC0vEgtcMqNfQ"
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false&key=%s" % (lat, lon, key)
    v = urllib.request.urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    return town, country

#def get_locations_nearby_coords(latitude, longitude, max_distance=None):
def get_locations_nearby_coords(location,max_distance = None) : 
    latlng = geocode(str(location))
    latlng = latlng.split(',')
    latitude, longitude =float(latlng[0]) , float(latlng[1])
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    # Great circle distance formula
    gcd_formula = "6371 * acos(cos(radians(%s)) * cos(radians(lat)) * cos(radians(lon) - radians(%s)) + sin(radians(%s)) * sin(radians(lat)))"
    distance_raw_sql = RawSQL(
        gcd_formula,
        (latitude, longitude, latitude)
    )
    qs = Pet.objects.all() \
    .annotate(distance=distance_raw_sql) \
    .order_by('distance')
    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance)
    return qs, distance_raw_sql


@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    if connection.vendor == "sqlite":
        # sqlite doesn't natively support math functions, so add them
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)
        cf('least', 2, max)
        cf('greatest', 2, min)


def geocode(location):
        key = "AIzaSyBlu5QpKaxho5vC2yN871kC0vEgtcMqNfQ"
        output = "json"
        location = urllib.parse.quote(location)
        request = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=%s&language=ko&inputtype=textquery&fields=geometry&key=%s" % (location, key)
        data = urllib.request.urlopen(request).read()
        dlist = json.loads(data.decode('utf-8'))
        if dlist["status"] == "OK":
            return "%s,%s" % (dlist['candidates'][0]['geometry']['location']['lat'],\
                 dlist['candidates'][0]['geometry']['location']['lng'])
        else:
            return ','
