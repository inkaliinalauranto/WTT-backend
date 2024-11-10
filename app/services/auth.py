import uuid
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy import text
from app.dtos.auth import AuthUser, LoginReq
from app.db import DB
from app.utils.access_token import Token


# Salasanan cryptaukseen liittyvä funktio
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self, db: DB):
        self.db = db


    # Autentisoi käyttäjän login tiedot ja palauttaa True, mikäli käyttäjätunnus ja salasana ovat valideja
    def _authenticate_user(self, credentials: LoginReq):
        # Haetaan user usernamen perusteella, tämä on mahdollista, koska username on uniikki
        user = self.db.execute(
            text("SELECT * FROM user WHERE username = :username"),
            {"username": credentials.username}
        ).mappings().first()

        if not user:
            return False

        if not pwd_context.verify(credentials.password, user["password"]):
            return False

        # Kaikki ok
        return True


    def get_user_by_access_jti(self, access_jti):
        try:
            # Haetaan user access_tokenin perusteella.
            user = self.db.execute(
                text("SELECT * FROM user WHERE access_jti = :sub"),
                {"sub": access_jti}
            ).mappings().first()

            if not user:
                raise JWTError

            return AuthUser(
                id=user['id'],
                username=user['username'],
                role_id=user['role_id'],
                team_id=user['team_id']
            )

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )


    def login(self, credentials: LoginReq, token: Token):
        try:
            # Verifioidaan käyttäjän kirjautumistiedot
            verified = self._authenticate_user(credentials)
            if not verified:
                raise HTTPException(
                    status_code=401,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"}
                )

            # Generoidaan random access_jti, joka avulla luodaan token.
            access_jti = str(uuid.uuid4())
            access_token = token.create(data={"sub": access_jti, "type": "access", "exp": timedelta(days=30)})

            # Päivitetään access_jti tietokantaan kyseiselle käyttäjälle.
            # Tätä käytetään, kun haetaan sisäänkirjautunut käyttäjä tai halutaan kirjautua ulos
            self.db.execute(
                text("UPDATE user SET access_jti = :sub WHERE username = :username"),
                {"sub": access_jti, "username": credentials.username}
            )
            self.db.commit()

            # Haetaan AuthUser
            user = self.get_user_by_access_jti(access_jti)

            # Palautetaan AuthUser ja generoitu token.
            return user, access_token

        except Exception as e:
            self.db.rollback()
            raise e


    def logout(self, user):
        try:
            self.db.execute(
                text("UPDATE user SET access_jti = NULL WHERE user.id = :id"),
                {"id": user.id}
            )
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e


# Katso UsersReposiotrion alaosasta kommentointi näihin liittyen
def get_service(db: DB):
    return AuthService(db)


AuthServ = Annotated[AuthService, Depends(get_service)]