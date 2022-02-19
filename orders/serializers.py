"""Orders Serializers."""
# RestFramework
from rest_framework import serializers

# Python
from datetime import datetime
import pytz


# Models
from menus.models import Option
from orders.models import Order

# App
from backend_test.settings import APP_TZ
from backend_test.utils.timezone import get_local_timestamp_for_custom_hour
from backend_test.const import (
    EXCEED_TIME_ALLOWED,
    OPTION_DOES_NOT_EXIST,
    USER_ALREADY_HAS_AN_ORDER)


class OrdersModelSerializer(serializers.ModelSerializer):
    """Orders Model Serializer"""

    class Meta:
        model = Order
        fields = ("id", "created", "employee",
                  "selected_option", "customization", "menu")

    def validate(self, data):
        order = Order.objects.filter(
            menu=data["menu"].pk,
            employee=data["employee"])
        if order:
            raise serializers.ValidationError(USER_ALREADY_HAS_AN_ORDER)

        try:
            Option.objects.filter(menu=data["menu"]).get(
                pk=data["selected_option"].pk)
        except Exception:
            raise serializers.ValidationError(OPTION_DOES_NOT_EXIST)

        tz_satiago = pytz.timezone(APP_TZ)
        now = datetime.now(tz_satiago)
        created_tz = datetime.timestamp(now)
        # datetime.fromtimestamp(created_tz, tz_satiago)

        if created_tz > get_local_timestamp_for_custom_hour():
            raise serializers.ValidationError(EXCEED_TIME_ALLOWED)
        return data
