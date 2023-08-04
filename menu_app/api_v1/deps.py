from menu_app.db.session import session


def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()
