from datetime import datetime, timezone

from fastapi import Depends,HTTPException
from sqlalchemy import text
from typing import Annotated
from app.db import DB
from app import models
from app.services.auth import pwd_context


class UsersService:

    def __init__(self, db):
        self.db = db


    def create(self, user: models.User):
        try:
            # Löytyykö role tietokannasta
            """
            role_id = self.db.execute(
                text("SELECT id FROM roles WHERE id = :role_id"),
                {"role_id": user.role_id}
            ).mappings().first()
            """
            # .query(mitä palautetaan).filter(minkä perusteella).mitkärivit()
            role = self.db.query(models.Role).filter(models.Role.id == user.role_id).first()

            if role is None:
                raise HTTPException(status_code=404, detail="Role not found")

            user.role = role

            # Onko käyttäjänimi jo käytössä
            """
            user_in_db = self.db.execute(
                text("SELECT username FROM users WHERE username = :username"),
                {"username": user.username}
            ).mappings().first()
            """
            username = self.db.query(models.User.username).filter(models.User.username == user.username).first()

            if username is not None:
                raise HTTPException(status_code=409, detail="Username is taken")


            # Häshätään salasana
            hashed_pw = pwd_context.hash(user.password)
            user.password = hashed_pw

            # Voidaan suorittaa insert ja commitoida se.
            # Tallennetaan kyselystä palautunut id User modeliin.
            """
            user.id = self.db.execute(
                text("INSERT INTO users(username, password, first_name, last_name, email, role_id, team_id, created_at) "
                     "VALUES(:username, :password, :first_name, :last_name, email, :role_id, :team_id, NOW())"),
                {
                    "username": user.username,
                    "password": hashed_pw,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role_id": user.role_id,
                    "team_id": user.team_id
                }
            ).lastrowid
            """

            # Luodaan timestamp, joka on UTC 0 ja muotoiltu ja muunnettu mysqliin sopivaksi.
            user.created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')

            # Lisätään käyttäjä, joka on models.User instanssi.
            self.db.add(user)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e


# Initialisoidaan UsersRepository tietokantayhteyden kanssa
def get_service(db: DB):
    return UsersService(db)


# Tämän toimintaperiaate on sama kuin databasen luonnissa.
# Alla olevassa annotated funktiossa injektoidaan tietokantayhteys UsersServicelle.
# UsersService injektoidaan nyt välittämällä tämä muuttuja parametrinä controllerin functioon -> (service: UsersServ).
UsersServ = Annotated[UsersService, Depends(get_service)]