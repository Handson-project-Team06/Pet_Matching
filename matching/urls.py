from django.contrib import admin
from django.urls import path
from matching.views import *


app_name = 'matching'

urlpatterns = [
   path('home/', home, name='home'),
   #path('home/', PetListView.as_view(), name='home'),
   path('home/my_pet_list/', MyPetListView.as_view(), name='my_pet_list'),
   path('home/my_pet_list/pet_create/', PetCreateView.as_view(), name='pet_create'),
   path('home/my_pet_list/<int:pk>/', PetUpdateView.as_view(), name='pet_update'),
   path('home/my_pet_list/<int:pk>/delete/', PetDeleteView.as_view(), name='pet_delete'),
]