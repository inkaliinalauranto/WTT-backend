from app.db import DB
from app.dtos import schema


def get_test(db: DB):
    return db.query(schema.Test).all()
