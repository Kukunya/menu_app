from sqlalchemy import select

from menu_app.db.session import SessionLocal
from menu_app.models.dishes import Dishes
from menu_app.schemas.base_obj import BaseObj


async def get_item_counts(submenu_id,
                          db=SessionLocal()):

    query = select(Dishes.filter(
        Dishes.sub_menu_id == submenu_id).count())
    dishes_count_in = await db.execute(query)
    db.close()

    return dishes_count_in


class SubmenuObj(BaseObj):
    dishes_count: int = 0

    async def pre_calculate(self):
        self.dishes_count = await get_item_counts(self.id)

    # def __init__(self, **data):
    #     if 'id' in data:
    #         data['dishes_count'] = get_item_counts(data['id'])
    #     super().__init__(**data)
