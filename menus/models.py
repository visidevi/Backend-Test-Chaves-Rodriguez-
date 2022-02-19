"""Menus Models"""

# Django
from django.db import models
from django.db.models import CASCADE

# Python
import uuid



class Menu(models.Model):
    message=models.CharField(max_length=520)
    date=models.DateField(unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Option(models.Model):
    description=models.CharField(max_length=800)
    menu = models.ForeignKey(Menu, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.description}"
