from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mssql import TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base


# Tänne tehdään kirjaimellisesti tietokannan taulut
# Ne luodaan automaattisesti tietokantaan, jos niitä ei vielä ole luotu
# main.py tiedostossa suorituvan Base.metadata.create_all(bind=engine) kautta


Base = declarative_base()


class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(45), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    access_jti = Column(String(512))
    created_at = Column(TIMESTAMP, nullable=False)
    deleted_at = Column(TIMESTAMP)
    role_id = Column(Integer, ForeignKey("role.id"))
    team_id = Column(Integer, ForeignKey("team.id"))


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False, unique=True)

    role_id = relationship('User', back_populates='role_id')


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False, unique=True)
    organization_id = Column(Integer, ForeignKey("organization.id"))

    team_id = relationship('User', back_populates='team_id')


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False, unique=True)
