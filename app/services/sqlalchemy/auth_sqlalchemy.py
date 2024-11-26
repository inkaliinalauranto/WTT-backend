import uuid
from datetime import timedelta
from passlib.context import CryptContext
from app.custom_exceptions.authorization import CredentialsException
from app.dtos.auth import LoginReq
from app.db_mysql import DB
from app.models import User
from app.services.base_services.auth_base_service import AuthBaseService
from app.utils.access_token import Token


# Salasanan cryptaukseen liittyvä funktio
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthServiceSqlAlchemy(AuthBaseService):
    def __init__(self, db: DBMySql):
        self.db = db


    # Autentisoi käyttäjän login tiedot ja palauttaa True, mikäli käyttäjätunnus ja salasana ovat valideja
    # Tätä metodia ei ole AuthBaseServicellä, vaan on tämän servicen oma apumetodi, joka voitaisiin suorittaa
    # myös suoraan loginissa.
    def _authenticate_user(self, credentials: LoginReq):
        # Haetaan user usernamen perusteella, tämä on mahdollista, koska username on uniikki
        user = self.db.query(User).filter(User.username == credentials.username).first()

        if not user:
            raise CredentialsException("Could not validate credentials")

        if not pwd_context.verify(credentials.password, user.password):
            raise CredentialsException("Could not validate credentials")


    def login(self, credentials: LoginReq, token: Token) -> User and str:
        try:
            # Verifioidaan käyttäjän kirjautumistiedot
            self._authenticate_user(credentials)

            # Generoidaan random access_jti, joka avulla luodaan token.
            access_jti = str(uuid.uuid4())
            access_token = token.create(data={"sub": access_jti, "type": "access", "exp": timedelta(days=7)})

            # Haetaan User ja asetetaan sinne tokenin jwt token identifier.
            user = self.db.query(User).filter(User.username == credentials.username).first()
            # Tätä käytetään, kun haetaan sisäänkirjautunut käyttäjä tai halutaan kirjautua ulos
            user.access_jti = access_jti

            self.db.commit()

            # Palautetaan User ja generoitu token.
            return user, access_token

        except Exception as e:
            self.db.rollback()
            raise e


    def logout(self, user: User):
        try:
            user.access_jti = None
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e
