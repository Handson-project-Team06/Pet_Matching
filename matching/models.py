from django.db import models
from django.urls import reverse_lazy


# Create your models here.

class Pet(models.Model):
    MALE, FEMALE = 0, 1
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    breed = models.CharField(max_length=50)
    picture = models.ImageField(blank=False)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default=MALE)

    def __str__(self):
        return self.name
