
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.crud import get_test
from app.schemas import TestSchema
from .dp import SessionLocal, Base, engine


app = FastAPI()

#Create tables in the database
Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return "Terve kaikki!"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/checkconnection")
async def read_root(db: Session = Depends(get_db)):
    return {"message": "Connected to MySQL"}

@app.get("/test", response_model=list[TestSchema])
def read_test(db: Session = Depends(get_db)):
    test = get_test(db)
    return test