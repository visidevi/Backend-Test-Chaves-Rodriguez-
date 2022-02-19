"""Menus Views"""

# RestFramework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


# Models
from menus.models import Menu, Option

# Permissions
from api.permissions import IsNora

# Serializers
from menus.serializers import (
    DetailMenuOptionsSerializer,
    DetailMenuSerializer,
    MenuSerializer,
    OptionSerializer,
)


class MenusViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsNora]

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return DetailMenuSerializer
        if self.action == "set_option":
            return OptionSerializer
        else:
            return self.serializer_class

    @action(detail=True, methods=["POST"], url_path="set-option")
    def set_option(self, request, pk: int):
        """Create an option for a specific menu

        Args:
            pk (int): menu UUID
            description (str): Option description

        Returns:
            HTTP Response 200 OK
        """
        data = {"menu": pk,
                "description": (request.data.get("description"))}

        serializer = self.get_serializer_class()(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class OptionsViewSet(ModelViewSet):
    """Options ViewSet"""
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated, IsNora]


class MenuView(APIView):
    """Menu View without permissions for employee"""
    permission_classes = []

    def get(self, request, uuid):
        menu = Menu.objects.get(pk=uuid)
        serializer = DetailMenuOptionsSerializer(menu)
        return Response(serializer.data)
