# models.py
from sqlalchemy import Column, Integer, String
from .dp import Base

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)