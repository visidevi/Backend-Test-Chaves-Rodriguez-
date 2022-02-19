"""Api Router"""

# RestFramework
from rest_framework.routers import DefaultRouter

# App Views
from orders.views import OrderViewSet
from employees.views import EmployeeViewSet
from menus.views import MenusViewSet, OptionsViewSet

router = DefaultRouter()

router.register(prefix="menus", basename="menus", viewset=MenusViewSet)
router.register(prefix="options", basename="options", viewset=OptionsViewSet)
router.register(prefix="employees", basename="employees",
                viewset=EmployeeViewSet)
router.register(prefix="orders", basename="orders", viewset=OrderViewSet)
