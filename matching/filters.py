from matching.models import Pet,GENDER_CHOICES 
import django_filters
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy
from django.db.models.expressions import RawSQL

import math
from django.db.backends.signals import connection_created
from django.dispatch import receiver

from math import radians, cos, sin, asin, sqrt



class PetFilter(django_filters.FilterSet):
    breed = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.ChoiceFilter(choices=GENDER_CHOICES,empty_label=ugettext_lazy(u'Any'))
    class Meta:
        model = Pet
        fields = ['breed', 'gender', ]

def get_locations_nearby_coords(latitude, longitude, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    # Great circle distance formula
    gcd_formula = "6371 * acos(cos(radians(%s)) * cos(radians(lat)) * cos(radians(longi) - radians(%s)) + sin(radians(%s)) * sin(radians(lat)))"
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
