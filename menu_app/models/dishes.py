from sqlalchemy import DECIMAL, VARCHAR, Column, ForeignKey

from menu_app.db.base_class import Base


class Dishes(Base):
    __tablename__ = 'dishes'
    id = Column(VARCHAR,
                primary_key=True)
    title = Column(VARCHAR,
                   unique=True)
    description = Column(VARCHAR)
    price = Column(DECIMAL)
    main_menu_id = Column(VARCHAR,
                          ForeignKey('menus.id', ondelete='CASCADE'))
    sub_menu_id = Column(VARCHAR,
                         ForeignKey('submenus.id', ondelete='CASCADE'))
