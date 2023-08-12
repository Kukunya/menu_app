from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_app.models.dishes import Dishes
from menu_app.models.menus import Menus
from menu_app.models.submenus import Submenus
from menu_app.schemas.base_obj import BaseObj
from menu_app.schemas.dish_obj import DishObj


class CRUDBase:
    def __init__(self, model, cache):
        self.model = model
        self.cache = cache

    async def get_item(self,
                       *id: str,
                       db: AsyncSession)\
            -> Menus | Submenus | Dishes | dict | None:

        db_id = id[-1]

        item = await self.cache.get_item(id)
        if item:
            return item

        item = await db.get(self.model, db_id)
        if item:
            item = await self.pre_calculate(db, item)
            await self.cache.add_item(data=item, id=id)
            return item

        return None

    async def add(self,
                  db: AsyncSession,
                  data: BaseObj | DishObj,
                  **id) \
            -> BaseObj | DishObj:

        item = data.model_dump()
        item.update(id)

        item = self.model(**item)
        db.add(item)
        await db.commit()
        await db.refresh(item)

        return data

    async def update(self,
                     *id: str,
                     db: AsyncSession,
                     data: BaseObj | DishObj) -> dict | None:

        db_id = id[-1]

        db_item = await db.get(self.model, db_id)
        if db_item:
            item = data.model_dump(exclude='id')
            for column, row in item.items():
                setattr(db_item, column, row)

            await db.commit()
            # CacheMenu.update_item(id=id, data=item)

            return {'id': db_id, **item}

        return None

    async def delete(self,
                     *id: str,
                     db: AsyncSession) -> bool:

        db_id = id[-1]

        item = await db.get(self.model, db_id)
        if item:
            await db.delete(item)
            await db.commit()
            # menu_cache.delete_item(id)
            return True
        return False

    async def is_item_exist(self, db: AsyncSession,
                            title: str) -> bool:

        query = select(self.model).filter(
            self.model.title == title)

        item = await db.execute(query)
        return bool(item.scalar())

    @staticmethod
    async def pre_calculate(db: AsyncSession,
                            item):
        return BaseObj.model_validate(item)
