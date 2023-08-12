from sqlalchemy import distinct, func, select

from menu_app.db.session import SessionLocal
from menu_app.models.dishes import Dishes
from menu_app.models.submenus import Submenus
from menu_app.schemas.base_obj import BaseObj


async def get_item_counts(main_menu_id,
                          db=SessionLocal()):

    query = select(
        func.count(distinct(Submenus.title)),
        func.count(distinct(Dishes.title))).join(
        Dishes, isouter=True).filter(
        Submenus.main_menu_id == main_menu_id,
        Dishes.main_menu_id == main_menu_id)
    items_count_in = await db.execute(query)
    db.close()

    return items_count_in


class MenuObj(BaseObj):
    submenus_count: int = 0
    dishes_count: int = 0

# class PreCalculateMenu(MenuObj):
#
#     def __init__(self, **data):
#         if 'id' in data:
#             data['submenus_count'], data['dishes_count'] = get_item_counts(data['id'])
#         super().__init__(**data)
