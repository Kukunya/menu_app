from typing import Union
from menu_app.schemas.base_obj import BaseObj
from menu_app.api_v1 import deps
from fastapi import Depends
from menu_app.models.dishes import Dishes


def get_item_counts(submenu_id,
                    db=Depends(deps.get_db)):
    return db.query(Dishes).filter(Dishes.sub_menu_id == submenu_id).count()


class SubmenuObj(BaseObj):
    dishes_count: Union[int, None] = None

    def __init__(self, **data):
        data['dishes_count'] = get_item_counts(data['id'])
        super().__init__(**data)
