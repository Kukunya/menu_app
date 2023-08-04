from typing import Union
from menu_app.schemas.base_obj import BaseObj
from sqlalchemy import distinct, func
from menu_app.api_v1 import deps
from fastapi import Depends
from menu_app.models.submenus import Submenus
from menu_app.models.dishes import Dishes


def get_item_counts(main_menu_id,
                    db=Depends(deps.get_db)):
    items_count_in = db.query(
        func.count(distinct(Submenus.title)),
        func.count(distinct(Dishes.title))).join(Dishes, isouter=True).filter(
        Submenus.main_menu_id == main_menu_id,
        Dishes.main_menu_id == main_menu_id).first()
    return items_count_in


class MenuObj(BaseObj):
    submenus_count: int = None
    dishes_count: int = None

    def __init__(self, **data):
        data['id'] = 0
        data['submenus_count'], data['dishes_count'] = 100, 100
        super().__init__(**data)
