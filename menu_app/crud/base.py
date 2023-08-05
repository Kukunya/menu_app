from sqlalchemy.orm import Session


class CRUDBase:
    def __init__(self, model):
        self.model = model

    def get_item(self, db: Session, id):

        item = db.query(self.model).filter(self.model.id == id).first()
        if item:
            return item

    def update(self, db: Session, data, id):
        item = db.query(self.model).filter(self.model.id == id).first()
        if item:
            item.title = data.title
            item.description = data.description
            db.commit()
            return item

    def delete(self, db: Session, id):
        if db.query(self.model).filter(self.model.id == id).delete():
            db.commit()
            return True

    def is_exist(self, db: Session, title):
        return db.query(self.model).filter(self.model.title == title).first()
