from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'matching'

urlpatterns = [
   path('home/', home, name='home'),
]