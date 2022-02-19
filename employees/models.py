# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django_countries.fields import CountryField

class Employee(models.Model):
    """Employee model.
    """
    username = models.CharField(unique=True, max_length=50)
    channel  = models.CharField(unique=True, max_length=50)
    tz = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)

    # Stats
    ordered_menus = models.PositiveIntegerField(default=0)
    def __str__(self):
        """Return username."""
        return self.username
