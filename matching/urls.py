from django.contrib import admin
from django.urls import path
import matching.views

app_name="matching"
urlpatterns = [
   path('', matching.views.home, name='home'),
]