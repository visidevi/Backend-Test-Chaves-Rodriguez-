"""Orders Models"""

# Django
from django.db import models


# Models
from menus.models import Menu, Option
from employees.models import Employee


class Order(models.Model):
    created = models.DateTimeField(
        auto_now=True,
        help_text="Date time on which the object was created.",
    )
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    customization = models.CharField(max_length=500, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
