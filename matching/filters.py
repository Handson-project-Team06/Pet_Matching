from matching.models import Pet
import django_filters
from django_filters import FilterSet, CharFilter, ChoiceFilter
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy


class PetFilter(FilterSet):
    class Meta:
        model = Pet
        fields = {
            'breed': ['contains'],
            'gender': ['exact'],
        }
