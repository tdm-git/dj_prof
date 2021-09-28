from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='user_image', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    lange = models.CharField(max_length=3, default='RUS')
