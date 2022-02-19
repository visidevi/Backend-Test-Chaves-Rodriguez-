"""Employees Serializer """
# RestFramework
from rest_framework import serializers


# Models
from employees.models import Employee



class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ("id", "username", "channel", "tz")
