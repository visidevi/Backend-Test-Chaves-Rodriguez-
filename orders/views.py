"""Orders views"""
# RestFramework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

# Python
import json

# Models
from menus.models import Menu, Option
from orders.models import Order
from employees.models import Employee


# App
from backend_test.utils.timezone import get_datetime_for_custom_timezone
from backend_test.http import post
from api.permissions import IsNora
from backend_test.webhook import get_blocks_of_daily_menu
from slack.models import Payload
from backend_test.const import (
    CAN_CUSTOMIZE,
    CREATED_SUCCESSFULLY,
    SLACK_ORDER_ERROR,
    SLACK_SELECT_OPTION_ERROR)

# Serializers
from orders.serializers import (
    OrdersModelSerializer
)


class OrderViewSet(ModelViewSet):
    """Orders viewset"""
    queryset = Order.objects.all()
    serializer_class = OrdersModelSerializer
    permission_classes = [IsAuthenticated, IsNora]


class OrderView(APIView):
    """Slack sdk integration
    Allows the user to create an order from the slack chat window
    Returns a successful or failed response when the order does not meet the validations
    """
    permission_classes = []

    def post(self, request, format=None):
        querydict = request.data
        payload = Payload.parse_obj(json.loads(querydict["payload"]))

        actions = payload.actions
        user = payload.user
        user_id = user.id
        response_url = payload.response_url
        response_payload = {
            "text": SLACK_ORDER_ERROR,
            "blocks": get_blocks_of_daily_menu()
        }
        option = list(filter(lambda x: x.block_id == "options", actions))
        if option:
            selected_option = option[0].selected_option.value
            # Selected option
            selected_option = Option.objects.get(id=int(selected_option))
            try:
                data = {
                    "employee": Employee.objects.get(channel=user_id).pk,
                    "menu": Menu.objects.get(date=get_datetime_for_custom_timezone()).pk,
                    "selected_option": selected_option.pk,
                }
                serializer = OrdersModelSerializer(data=data)
                is_valid = serializer.is_valid()
                if is_valid:
                    serializer.save()
                    response_payload = {

                        "text": f"{CAN_CUSTOMIZE} \n {selected_option.description}",
                        "blocks": [		{
                            "dispatch_action": True,
                            "type": "input",
                            "block_id": "customizations",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "plain_text_input-action",
                                "placeholder": {
                                        "type": "plain_text",
                                        "text": "e.g. no salad"
                                }
                            },
                            "label": {
                                "type": "plain_text",
                                "text": f"{CAN_CUSTOMIZE} **{selected_option.description}** \nSpecify customizations:",
                                "emoji": True
                            }
                        }]
                    }
                else:
                    errors = serializer.errors["non_field_errors"][0]
                    response_payload = {
                        "text": str(errors)
                    }
            except Exception as e:
                print(str(e))
        # Customization
        customization = list(
            filter(lambda x: x.block_id == "customizations", actions))
        if customization:
            customization = customization[0].value

            try:
                instance = Order.objects.get(
                    employee=Employee.objects.get(channel=user_id),
                    menu=Menu.objects.get(
                        date=get_datetime_for_custom_timezone()),
                )
                data = {
                    "customization": customization
                }
                serializer = OrdersModelSerializer(instance)
                update = serializer.update(instance, data)
                if update:
                    response_payload = {
                        "replace_original": "true",
                        "text": f"""{CREATED_SUCCESSFULLY}
                        \n **{instance.selected_option},\n - {serializer.data['customization']}**"""
                    }
                else:
                    errors = serializer.errors["non_field_errors"][0]
                    response_payload = {
                        "text": str(errors)
                    }

            except Exception as e:

                response_payload = {
                    "text": SLACK_SELECT_OPTION_ERROR
                }

        data = post(url=response_url, json=response_payload)
        return Response(data=data, status=status.HTTP_200_OK)
