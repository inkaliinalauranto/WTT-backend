from datetime import datetime, timezone
from fastapi import Depends, HTTPException
from sqlalchemy import text, func
from typing import Annotated
from app.db import DB
from app import models
from app.models import Shift, ShiftType, User
from app.services.auth import pwd_context


class UsersService:

    def __init__(self, db):
        self.db = db

    # Haetaan käyttäjä id:n perusteella:
    def get_by_id(self, user_id):
        """"
        SELECT * FROM users WHERE id = {user_id}
        """
        user_id_tuple = (self.db.query(User).filter(User.id == user_id)).first()
        return user_id_tuple

    # Haetaan id:n perusteella käyttäjän kuluvan viikon suunnitellut työvuorot:
    def get_planned_shifts_by_id(self, user_id):
        # Tarkistetaan ensin, löytyykö käyttäjää. get_by_id palauttaa Nonen,
        # jos käyttäjää haetulla id:llä ei ole olemassa:
        user = self.get_by_id(user_id)

        if user is None:
            return None

        """
        SELECT s.start_time, s.end_time FROM shifts s
        JOIN shift_types st ON s.shift_type_id = st.id
        JOIN users u ON s.user_id = u.id
        WHERE u.id = {user_id}
        AND st.type = "planned"
        AND YEARWEEK(s.start_time, 1) = YEARWEEK(CURRENT_TIMESTAMP(), 1)
        """

        shift_times = (self.db.query(Shift.start_time, Shift.end_time)
                       .join(ShiftType, Shift.shift_type_id == ShiftType.id)
                       .join(User, Shift.user_id == User.id)
                       .filter(User.id == user_id,
                               ShiftType.type == "planned",
                               func.yearweek(Shift.start_time, 1) == func.yearweek(func.current_timestamp(), 1))).all()

        planned_shift_dicts_list = [{"start_time": shift.start_time, "end_time": shift.end_time} for shift in
                                    shift_times]

        return planned_shift_dicts_list

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
