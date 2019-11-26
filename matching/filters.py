from matching.models import Pet, GENDER_CHOICES
import django_filters
from django_filters import FilterSet, CharFilter, ChoiceFilter
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy


class PetFilter(FilterSet):
    breed = CharFilter(lookup_expr='icontains')
    gender = ChoiceFilter(choices=GENDER_CHOICES,empty_label=ugettext_lazy(u'Any'))
    class Meta:
        model = Pet
        fields = ['breed', 'gender', ]