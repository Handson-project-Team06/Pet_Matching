from django.db import models

# Create your models here.
class Pets(models.Model):
    objects=models.Manager()
    name=models.CharField(max_length=30)
    #pic=models.ImageField(blank=False,)
    #owner=models.ForeignKey(User)

    def __str__(self):
        return self.name