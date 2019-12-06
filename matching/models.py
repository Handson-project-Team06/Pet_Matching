from django.db import models
from django.urls import reverse_lazy

# Create your models here.
MALE, FEMALE = 'M', 'F'
GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
DOG, CAT = 'dog', 'cat'
ANIMAL_CHOICES = (
    (DOG, 'dog'),
    (CAT, 'cat'),
)
class Pet(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    animal = models.CharField(choices=ANIMAL_CHOICES, null=False , max_length=10)
    gender = models.CharField(choices=GENDER_CHOICES, null=False , max_length=4)
    breed = models.CharField(max_length=50)
    picture = models.ImageField(blank=False)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    address = models.CharField(max_length=200, null=False, default = '')
    introduction = models.CharField(max_length=300)
    def __str__(self):
        return self.name
