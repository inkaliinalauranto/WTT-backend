import os
from typing import Annotated
import dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

dotenv.load_dotenv()

# DB_USER = os.getenv("MYSQL_USER")
# DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
# DB_HOST = os.getenv("MYSQL_DATABASE")
# DB_NAME = os.getenv("MYSQL_DATABASE_NAME")
#
# database_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = None
    try:
        db = session()
        yield db
    finally:
        db.close()


DbMySql = Annotated[Session, Depends(get_db)]
