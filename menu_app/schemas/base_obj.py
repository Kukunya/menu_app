from pydantic import BaseModel
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
