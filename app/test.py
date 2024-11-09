from sqlalchemy import Column, Integer, String
from app.services.db import Base


class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
