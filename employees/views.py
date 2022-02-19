"""Employees views."""
# RestFramework
from api.permissions import IsNora
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

# Models
from employees.models import Employee

# Serializers
from employees.serializers import (
    EmployeeSerializer
)


class EmployeeViewSet(ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsNora]
