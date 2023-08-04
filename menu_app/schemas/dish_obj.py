from decimal import Decimal
from menu_app.schemas.base_obj import BaseObj


class DishObj(BaseObj):
    price: Decimal
