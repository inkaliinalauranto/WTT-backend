from os import access
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app import models
from app.services.users import UsersServ
from app.utils.access_token import Token


# Autorisaatio skeema. Route on sama, kuin openapin kautta tehtävä login.
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login/openapi', auto_error=False)


def get_user_by_access_jti(token: Token, service: UsersServ, req: Request, auth: Annotated[str, Depends(oauth_scheme)] = None):
    # Asetetaan access_tokeniksi keksistä löytyvä token
    # Ja käytetään sitä ensisijaisesti. Vaihtoehtoisesti tarkastetaan, tuliko authorization bearerin mukana token.
    access_token = req.cookies.get("wtt-cookie")

    # Tarkistetaan, löytyykö Authorization Bearer token.
    if not access_token:
        access_token = auth
        if not auth:
            raise HTTPException(status_code=401, detail="Unauthorized access")

    try:
        # Tarkistetaan onko token meidän luoma
        payload = token.verify(access_token)
        if payload['type'] != 'access':
            raise HTTPException(status_code=401, detail="Unauthorized access")

        # Tarkistetaan onko käyttäjä kirjautunut sisään
        user = service.get_user_by_access_jti(payload['sub'])
        if user is None:
            raise HTTPException(status_code=401, detail="Unauthorized access")

    # Token ei ole validi
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # models.User
    return user


# LoggedInUser on AuthUser, johon on suoritettu get_user_by_access_jti functio, eli se on autorisoitu käyttäjä.
LoggedInUser = Annotated[models.User, Depends(get_user_by_access_jti)]
