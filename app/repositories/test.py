from app import schema
from app.services.db import DB


def get_test(db: DB):
    return db.query(schema.Test).all()
