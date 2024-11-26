import os
from typing import Annotated
import dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


dotenv.load_dotenv()

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
# Jotta toimi (Inka-Liinalla), oli MY_SQL_DATABASE-ympäristömuuttujan arvo
# vaihdettava "db":ksi:
# DB_HOST = "db"
DB_HOST = os.getenv("MYSQL_DATABASE")
DB_NAME = os.getenv("MYSQL_DATABASE_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = None
    try:
        db = session()
        yield db
    finally:
        db.close()


DB = Annotated[Session, Depends(get_db)]
