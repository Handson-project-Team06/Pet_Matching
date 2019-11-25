from matching.models import Pet,GENDER_CHOICES 
import django_filters
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy


class PetFilter(django_filters.FilterSet):
    breed = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.ChoiceFilter(choices=GENDER_CHOICES,empty_label=ugettext_lazy(u'Any'))
    class Meta:
        model = Pet
        fields = ['breed', 'gender', ]
        