from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_app.cache.crud.cache_dishes import dish_cache
from menu_app.crud.base import CRUDBase
from menu_app.models.dishes import Dishes
from menu_app.schemas.dish_obj import DishObj


class CRUDDishes(CRUDBase):
    async def get_items(self,
                        top_id: str,
                        db: AsyncSession) -> list[DishObj]:

        query = select(self.model).filter(
            self.model.sub_menu_id == top_id)

        items = await db.execute(query)

        return [await self.pre_calculate(db=db,
                                         dish=dish)
                for dish in items.scalars()]

    @staticmethod
    async def pre_calculate(db: AsyncSession,
                            dish):
        return DishObj.model_validate(dish)


dishes = CRUDDishes(model=Dishes,
                    cache=dish_cache)
