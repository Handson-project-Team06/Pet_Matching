from django.shortcuts import render
from matching.models import Pet
from matching.filters import PetFilter,get_locations_nearby_coords
# Create your views here.

def home(request):
    pet_list=Pet.objects.all()
    pet_filter = PetFilter(request.GET,queryset=pet_list)
    nearby_locations , distance = get_locations_nearby_coords(48.8582, 2.2945, 5)
    return render(request,'home.html',{'filter':pet_filter, 'nearby_locations':nearby_locations, 'distance':distance})

