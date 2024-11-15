from datetime import datetime, timezone
from os import environ
from typing import Annotated
from fastapi.params import Depends
from jose import jwt


class AccessToken:
    def __init__(self, secret_key):
        self.secret_key = secret_key


    # Luodaan access token, jota käytetään autentisontiin. Tokenille voidaan määritellä vanhentumisaika
    # Muista createssa antaa dataksi esim. {"sub": access_jti, "type": "access", "exp": timedelta(days=30)}
    def create(self, data: dict):
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + data['exp']
        to_encode.update({"iss": "WorktimeTracker", "aud": "WorktimeTracker", "exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm='HS512')

        return token


    def verify(self, token):
        payload = jwt.decode(
            token, self.secret_key, algorithms=['HS512'], audience="WorktimeTracker", issuer="WorktimeTracker"
        )
        return payload


# Injectoidaan tässä salainen avain tokenien käsittelyyn
def get_token():
    return AccessToken(environ.get("SECRET_KEY"))


Token = Annotated[AccessToken, Depends(get_token)]
