from menu_app.db.session import session
from menu_app.models.dishes import Dishes
from menu_app.schemas.base_obj import BaseObj


def get_item_counts(submenu_id,
                    db=session()):
    dishes_count_in = db.query(Dishes).filter(
        Dishes.sub_menu_id == submenu_id).count()
    db.close()
    return dishes_count_in


class SubmenuObj(BaseObj):
    dishes_count: int | None = None

    def __init__(self, **data):
        if 'id' in data:
            data['dishes_count'] = get_item_counts(data['id'])
        super().__init__(**data)
