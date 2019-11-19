from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField('핸드폰 번호', max_length=13)
    birth_date = models.DateField('생년월일')
    name = models.CharField('이름', max_length=15)