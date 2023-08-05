from sqlalchemy import distinct, func

from menu_app.db.session import session
from menu_app.models.dishes import Dishes
from menu_app.models.submenus import Submenus
from menu_app.schemas.base_obj import BaseObj


def get_item_counts(main_menu_id,
                    db=session()):
    items_count_in = db.query(
        func.count(distinct(Submenus.title)),
        func.count(distinct(Dishes.title))).join(Dishes, isouter=True).filter(
        Submenus.main_menu_id == main_menu_id,
        Dishes.main_menu_id == main_menu_id).first()
    db.close()
    return items_count_in


class MenuObj(BaseObj):
    submenus_count: int | None = None
    dishes_count: int | None = None

    def __init__(self, **data):
        if 'id' in data:
            data['submenus_count'], data['dishes_count'] = get_item_counts(data['id'])
        super().__init__(**data)
