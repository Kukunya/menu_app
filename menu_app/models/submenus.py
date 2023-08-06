from sqlalchemy import VARCHAR, Column, ForeignKey

from menu_app.db.base_class import Base


class Submenus(Base):
    __tablename__ = 'submenus'
    id = Column(VARCHAR, primary_key=True)
    title = Column(VARCHAR, unique=True)
    description = Column(VARCHAR)
    main_menu_id = Column(VARCHAR,
                          ForeignKey('menus.id', ondelete='CASCADE'))
