from app.db_mysql import DB
from app.models import Test


def get_test(db: DB):
    return db.query(Test).all()
