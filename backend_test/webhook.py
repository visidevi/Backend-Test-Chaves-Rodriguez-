from backend_test.utils.timezone import get_datetime_for_custom_timezone
from datetime import datetime
from menus.models import Menu, Option
from employees.models import Employee
from backend_test.settings import APP_TZ, SLACK_APP_TOKEN
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pytz import timezone
import logging
logger = logging.getLogger(__name__)

client = WebClient(token=SLACK_APP_TOKEN)


def send_daily_menu():
    employees = fetch_employees()
    blocks = get_blocks_of_daily_menu()
    for employee in employees:
        send_notification(employee, blocks)


def send_notification(user, blocks):
    try:
        result = client.chat_postMessage(
            channel=user.channel,
            text=f"Hello again :wave: {user.username}",
            blocks=blocks
        )
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")


def fetch_employees():
    try:
        users = client.users_list()
        data = users.data["members"]
        chilean_employees = [user for user in data if user["tz"] == APP_TZ and not user["deleted"]]
        for employee in chilean_employees:

            # Valid if the user exists in the database and if it does not exist it creates it
            Employee.objects.get_or_create(
                username=employee["real_name"],
                channel=employee["id"],
                tz=employee["tz"],
                deleted=employee["deleted"]
            )
        return Employee.objects.all()

    except SlackApiError as e:
        logger.error("Error fetching conversations: {}".format(e))


def get_blocks_of_daily_menu():
    """ Returns a list of blocks for the daily menu"""
    try:
        date = get_datetime_for_custom_timezone()

        options = Option.objects.filter(menu__date=date).all()
        if options:
            block_options = []
            for option in options:
                block_option = {
                    "text": {
                        "type": "plain_text",
                                "text": option.description,
                                "emoji": True
                    },
                    "value": str(option.pk)
                }
                block_options.append(block_option)
            uuid_menu = Menu.objects.get(date=date).pk
            url_menu = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Today's menu :\n*<http://127.0.0.1:8000/menu/{uuid_menu}|https://nora.cornershop.io/menu/{uuid_menu}>*"
                }
            }
            return get_blocks(url_menu, block_options)
        else:
            return None
    except Exception as e:
        logger.error(f"Error fetching menu: {e}")


def get_blocks(url, options):
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Hello! \n I share with you today's menu :)",
                "emoji": True
            }
        },
        {
            "type": "divider"
        },
        url,
        {
            "type": "divider"
        },
        {
            "type": "input",
            "block_id": "options",
                        "element": {
                            "type": "radio_buttons",
                            "options": options,
                            "action_id": "radio_buttons-action"
                        },
                    "label": {
                            "type": "plain_text",
                            "text": "Options",
                            "emoji": True
                            }
        },
        {
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
                            "text": "Specify customizations",
                            "emoji": True
                            }
        }
    ]
