from decimal import Decimal

from menu_app.schemas.base_obj import BaseObj

# def json_dump(*args, **kwargs):
#     res = json.dumps(*args, **kwargs, use_decimal=True)
#     return res


class DishObj(BaseObj):
    price: Decimal

    # class Config:
    #     arbitrary_types_allowed = True
    #     json_dumps = json_dump
