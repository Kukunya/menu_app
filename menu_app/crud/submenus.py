from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_app.cache.crud.cache_submenus import submenu_cache
from menu_app.crud.base import CRUDBase
from menu_app.models.dishes import Dishes
from menu_app.models.submenus import Submenus
from menu_app.schemas.submenu_obj import SubmenuObj


class CRUDSubmenus(CRUDBase):
    async def get_items(self,
                        top_id: str,
                        db: AsyncSession):

        query = select(self.model).filter(
            self.model.main_menu_id == top_id)

        items = await db.execute(query)

        return [await self.pre_calculate(db=db,
                                         submenu=submenu)
                for submenu in items.scalars()]

    @staticmethod
    async def pre_calculate(db: AsyncSession,
                            submenu: Submenus):

        async def get_item_counts(id):
            query = select(Dishes).filter(
                Dishes.sub_menu_id == id)
            dishes_count_in = await db.execute(query)

            return len(dishes_count_in.fetchall())

        submenu = SubmenuObj.model_validate(submenu)
        submenu.dishes_count = await get_item_counts(submenu.id)

        return submenu


submenus = CRUDSubmenus(model=Submenus,
                        cache=submenu_cache)
