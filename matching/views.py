from django.shortcuts import render
from matching.models import Pet
from matching.filters import PetFilter
# Create your views here.

def home(request):
    pet_list=Pet.objects.all()
    pet_filter = PetFilter(request.GET,queryset=pet_list)
    return render(request,'home.html',{'filter':pet_filter})

