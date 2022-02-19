"""Menus Serializers"""

# rest_framework
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


# Models
from menus.models import Menu, Option


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ("id", "description", "menu")

    def validate(self, data):
        option = Option.objects.filter(
            menu=data["menu"],
            description=data["description"])
        if option:
            raise serializers.ValidationError("La opción ya existe")
        return data


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("id", "message", "date")


class DetailMenuSerializer(serializers.ModelSerializer):
    """Returns the options and orders of the menu"""
    options = SerializerMethodField()

    def get_options(self, instance):
        return list(instance.option_set.values("id", "description"))

    orders = SerializerMethodField()

    def get_orders(self, instance):
        return list(instance.order_set.values("employee__username", "customization", "selected_option__description"))

    class Meta:
        model = Menu
        fields = ("id", "message", "date", "options", "orders")


class DetailMenuOptionsSerializer(serializers.ModelSerializer):
    """ Cliente View
    Returns the options and orders of the menu
    """
    options = SerializerMethodField()

    def get_options(self, instance):
        return list(instance.option_set.values("id", "description"))

    class Meta:
        model = Menu
        fields = ("id", "date", "options")
