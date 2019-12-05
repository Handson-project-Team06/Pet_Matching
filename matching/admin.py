from django.contrib import admin
from matching.models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    pass
