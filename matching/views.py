from django.shortcuts import render
from .models import Pet
from .filters import PetFilter
# Create your views here.

def home(request):
    pet_list = Pet.objects.all()
    pet_filter = PetFilter(request.GET,queryset=pet_list)
    return render(request,'matching/home.html',{'filter':pet_filter})

