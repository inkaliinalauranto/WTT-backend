from datetime import datetime, timezone
from fastapi import Depends, HTTPException
from typing import Annotated
from app.db import DB
from app.dtos.auth import AuthUser
from app.models import User, Role
from app.services.auth import pwd_context


class UsersService:
    def __init__(self, db):
        self.db = db

    # Haetaan käyttäjä id:n perusteella:
    def get_by_id(self, user_id: int) -> User:
        """"
        SELECT * FROM users WHERE id = {user_id}
        """
        user = (self.db.query(User).filter(User.id == user_id)).first()
        return user


    def get_all_by_team_id(self, team_id:int) -> list[AuthUser]:
        employee_role = self.db.query(Role).filter(Role.name == "employee").first()
        users = self.db.query(User).filter(User.team_id == team_id, User.role_id == employee_role.id).all()

        users_list: list[AuthUser] = []
        for user in users:
            users_list.append(AuthUser.model_validate(user))

        return users_list


    def create(self, user: User):
        try:
            # Löytyykö role tietokannasta
            """
            role_id = self.db.execute(
                text("SELECT id FROM roles WHERE id = :role_id"),
                {"role_id": user.role_id}
            ).mappings().first()
            """
            # .query(mitä palautetaan).filter(minkä perusteella).mitkärivit()
            role = self.db.query(Role).filter(Role.id == user.role_id).first()

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
            username = self.db.query(User.username).filter(User.username == user.username).first()

            if username is not None:
                raise HTTPException(status_code=409, detail="Username is taken")

            # Häshätään salasana
            hashed_pw = pwd_context.hash(user.password)
            user.password = hashed_pw

            # Luodaan timestamp, joka on UTC 0 ja muotoiltu ja muunnettu mysqliin sopivaksi.
            user.created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')

            """
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
            """
            # Lisätään käyttäjä, joka on models.User instanssi.
            self.db.add(user)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e


    def get_user_by_access_jti(self, access_jti):
        # Haetaan user access_tokenin perusteella.
        user = self.db.query(User).filter(User.access_jti == access_jti).first()
        """
              user = self.db.execute(
                  text("SELECT * FROM users WHERE access_jti = :sub"),
                  {"sub": access_jti}
              ).mappings().first()
              """
        return user
    

    def delete_user_by_id(self, user_id: int, manager:User):
        try:
            # Haetaan asyncisti id:n perusteella poistettava käyttäjä
            user = self.get_by_id(user_id)

            if user is None:
                # Jos käyttäjää ei ole, palautetaan 404
                raise HTTPException(status_code=404, detail="User not found")

            if manager.role_id == user.role_id:
                # Jos käyttäjän rooli on sama kuin poistettavan rooli, tämä on kiellettyä.
                raise HTTPException(status_code=403, detail="Unauthorized action")
            
            # Jos käyttäjä löytyy, poistetaan se
            self.db.delete(user)
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
