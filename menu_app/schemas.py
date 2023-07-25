from pydantic import BaseModel
from decimal import Decimal
from typing import Union
from uuid import UUID, uuid4


class BaseObj(BaseModel):
    id: Union[UUID, int, None] = None
    title: str
    description: str

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = uuid4()
        super().__init__(**data)


class MenuObj(BaseObj):
    submenus_count: Union[int, None] = None
    dishes_count: Union[int, None] = None


class SubmenuObj(BaseObj):
    dishes_count: Union[int, None] = None


class DishObj(BaseObj):
    price: Decimal


class RespErrNotFound(BaseModel):
    detail: str


class RespConfirmDel(BaseModel):
    status: bool
    message: str
