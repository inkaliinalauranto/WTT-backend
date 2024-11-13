from sqlalchemy import TIMESTAMP, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base


# Tänne tehdään kirjaimellisesti tietokannan taulut
# Ne luodaan automaattisesti tietokantaan, jos niitä ei vielä ole luotu
# main.py tiedostossa suorituvan Base.metadata.create_all(bind=engine) kautta


Base = declarative_base()


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(45), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    access_jti = Column(String(512))
    created_at = Column(TIMESTAMP, nullable=False)
    deleted_at = Column(TIMESTAMP)
    role_id = Column(Integer, ForeignKey("roles.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False, unique=True)


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False, unique=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False, unique=True)


class ShiftType(Base):
    __tablename__ = "shift_types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(45), nullable=False, unique=True)


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shift_type_id = Column(Integer, ForeignKey("shift_types.id"))
    description = Column(String(255), nullable=True)
