from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey
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
    role_id = Column(Integer, ForeignKey(column="roles.id", ondelete="CASCADE", onupdate="CASCADE"))
    team_id = Column(Integer, ForeignKey(column="teams.id", ondelete="CASCADE", onupdate="CASCADE"))


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False, unique=True)


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False, unique=True)
    organization_id = Column(Integer, ForeignKey(column="organizations.id", ondelete="CASCADE", onupdate="CASCADE"))


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
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE", onupdate="CASCADE"))
    shift_type_id = Column(Integer, ForeignKey(column="shift_types.id", ondelete="CASCADE", onupdate="CASCADE"))
    description = Column(String(255), nullable=True)
