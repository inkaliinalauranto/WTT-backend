# crud.py
from sqlalchemy.orm import Session
from .models import Test

def get_test(db: Session):
    return db.query(Test).all()
