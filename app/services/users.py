from fastapi import Depends,HTTPException
from sqlalchemy import text
from typing import Annotated
from app.db import DB
from app.dtos.users import User
from app.services.auth import pwd_context


class UsersService:

    def __init__(self, db):
        self.db = db


    def create(self, user: User):
        try:
            # Löytyykö role tietokannasta
            role_id = self.db.execute(
                text("SELECT id FROM roles WHERE id = :role_id"),
                {"role_id": user.role_id}
            ).mappings().first()

            if role_id is None:
                raise HTTPException(status_code=404, detail="Role not found")


            # Onko käyttäjänimi jo käytössä
            user_in_db = self.db.execute(
                text("SELECT username FROM users WHERE username = :username"),
                {"username": user.username}
            ).mappings().first()

            if user_in_db is not None:
                raise HTTPException(status_code=409, detail="Username is taken")


            # Häshätään salasana
            hashed_pw = pwd_context.hash(user.password)

            # Voidaan suorittaa insert ja commitoida se.
            # Tallennetaan kyselystä palautunut id User modeliin.
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
