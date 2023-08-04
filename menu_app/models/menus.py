from menu_app.db.base_class import Base
from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.postgresql import UUID


class Menus(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(VARCHAR, unique=True)
    description = Column(VARCHAR)
