from django.db import models

# Create your models here.
GENDER_CHOICES =(
        ('male','Male'),
        ('female','Female'),
    )
class Pet(models.Model):
    objects=models.Manager()
    name=models.CharField(max_length=30)
    age=models.IntegerField(default=0)
    weight=models.IntegerField(default=0)
    breed=models.CharField(max_length=50)
    pic=models.ImageField(blank=False)
    gender=models.CharField(("Gender"), max_length=80, choices=GENDER_CHOICES, null=True)
    #owner=models.ForeignKey(User)

    def __str__(self):
        return self.name