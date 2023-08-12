from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_app.cache.crud.cache_menus import menu_cache
from menu_app.crud.base import CRUDBase
from menu_app.models.dishes import Dishes
from menu_app.models.menus import Menus
from menu_app.models.submenus import Submenus
from menu_app.schemas.menu_obj import MenuObj


class CRUDMenus(CRUDBase):

    async def get_items(self,
                        db: AsyncSession)\
            -> list[MenuObj]:

        items = await db.execute(select(self.model))

        return [await self.pre_calculate(db=db,
                                         menu=menu)
                for menu in items.scalars()]

    @staticmethod
    async def pre_calculate(db: AsyncSession,
                            menu: Menus):

        async def get_item_counts(id):
            query = select(
                func.count(distinct(Submenus.title)),
                func.count(distinct(Dishes.title))).join(
                Dishes, isouter=True).filter(
                Submenus.main_menu_id == id,
                Dishes.main_menu_id == id)
            items_count_in = await db.execute(query)

            return items_count_in.fetchone()
        menu = MenuObj.model_validate(menu)
        menu.submenus_count, menu.dishes_count = await get_item_counts(menu.id)

        return menu


menus = CRUDMenus(model=Menus,
                  cache=menu_cache)
