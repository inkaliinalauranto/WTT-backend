from sqlalchemy.orm import Session
from app import test


def get_test(db: Session):
    return db.query(test.Test).all()
