# from typing import ClassVar
import json
from uuid import uuid4

from pydantic import BaseModel  # , ConfigDict


def json_dump(*args, **kwargs):
    res = json.dumps(*args, **kwargs, use_decimal=True)
    return res


class BaseObj(BaseModel):
    id: str
    title: str
    description: str

    # config_model: ClassVar[str] = ConfigDict(from_attributes=True)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_dumps = json_dump

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid4())
        super().__init__(**data)
