"""Test"""
# python
import datetime

# Django
from django.contrib.auth.models import User
from django.test import TestCase

# Rest Framework
from rest_framework import status

# APP
from backend_test.const import EXCEED_TIME_ALLOWED, USER_ALREADY_HAS_AN_ORDER


TODAYS_MENU = "Today's menu"


class TestMenu(TestCase):
    """Test Menu """
    fixtures = ['menus', 'users']

    def _generate_menu_with_option(self, date=datetime.date.today()):
        user = User.objects.get(pk=1)
        self.client.force_login(user)

        menu_dict = {
            "date": date,
            "message": TODAYS_MENU
        }
        menu = self.client.post('/api/menus/', menu_dict)
        menu_response_json = menu.json()

        # Option
        option_dict = {"description": "Option 1: Option de menu"}
        id_menu = menu_response_json.get("id")

        self.client.post(f'/api/menus/{id_menu}/set-option/', option_dict)
        response = self.client.get(f'/api/menus/{id_menu}/')
        return response.json()

    def test_retrieve_menu(self):
        response = self.client.get(
            f'/menu/4302203d-8262-4496-a17f-6b7ca8034658')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('options'), list)
        self.assertIsInstance(response_json.get('date'), str)
        self.assertIsInstance(response_json.get('id'), str)

        self.assertEqual(len(response_json.get('options')), 3)

    def test_create_menu(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        menu_dict = {
            "date": datetime.date.today(),
            "message": TODAYS_MENU
        }
        response = self.client.post('/api/menus/', menu_dict)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()

        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('date'), str)
        self.assertIsInstance(response_json.get('id'), str)
        self.assertEqual(response_json.get('message'), menu_dict.get('message'))

    def test_user_not_authorized(self):
        menu_dict = {
            "date": datetime.date.today(),
            "message": TODAYS_MENU
        }
        response = self.client.post('/api/menus/', menu_dict)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_set_option_to_menu(self):
        response_json = self._generate_menu_with_option()
        option = response_json.get('options')[0]

        # Menu with option
        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('options'), list)
        self.assertEqual(len(response_json.get('options')), 1)
        self.assertEqual(response_json.get('message'), TODAYS_MENU)

        # Option
        self.assertIsInstance(option, dict)
        self.assertIsInstance(option.get('id'), int)
        self.assertEqual(option.get('description'), "Option 1: Option de menu")

    def test_set_option_to_menu_with_no_order(self):
        response_json = self._generate_menu_with_option()
        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('orders'), list)
        self.assertEqual(len(response_json.get('orders')), 0)

    def test_create_order_after_11_am_error(self):
        menu_with_option = self._generate_menu_with_option()

        # Employee
        employee_dict = {
            "username": "example",
            "channel": "ExampleXX234",
            "tz": "America/Santiago",
            "email": "test123@test.cl"
        }
        employee = self.client.post('/api/employees/', employee_dict)
        employee_response_json = employee.json()

        # order
        order_dict = {
            "employee": employee_response_json.get("id"),
            "selected_option": menu_with_option.get("options")[0].get("id"),
            "menu": menu_with_option.get("id"),
            "customization": "Con ensalada y pebre"
        }
        response = self.client.post('/api/orders/', order_dict)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get("non_field_errors"), list)
        self.assertEqual(response_json.get("non_field_errors")
                         [0], EXCEED_TIME_ALLOWED)


class TestOrder(TestCase):
    """Orders Test Cases"""
    fixtures = ['menus', 'users']

    def test_retrieve_order(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(f'/api/orders/41/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('created'), str)
        self.assertIsInstance(response_json.get('id'), int)
        self.assertEqual(response_json.get('customization'),
                         'con ensalada y mucho amor')
        self.assertEqual(response_json.get('selected_option'), 5)
        self.assertEqual(response_json.get('employee'), 3)
        self.assertEqual(response_json.get('menu'),
                         '4302203d-8262-4496-a17f-6b7ca8034658')

    def test_create_order_error(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        orders_dict = {
            "employee": 3,
            "selected_option": 5,
            "customization": "con ensalada y mucho amor",
            "menu": "4302203d-8262-4496-a17f-6b7ca8034658"
        }

        response = self.client.post('/api/orders/', orders_dict)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_json = response.json()

        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get("non_field_errors"), list)
        self.assertEqual(response_json.get("non_field_errors")
                         [0], USER_ALREADY_HAS_AN_ORDER)
