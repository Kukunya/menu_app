from sqlalchemy import VARCHAR, Column

from menu_app.db.base_class import Base


class Menus(Base):
    __tablename__ = 'menus'
    id = Column(VARCHAR, primary_key=True)
    title = Column(VARCHAR, unique=True)
    description = Column(VARCHAR)
