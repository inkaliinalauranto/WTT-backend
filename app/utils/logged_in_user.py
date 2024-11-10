from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.dtos.auth import AuthUser
from app.services.auth import AuthServ
from app.utils.access_token import Token


# Autorisaatio skeema. Route on sama, kuin openapin kautta tehtävä login.
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login/openapi', auto_error=False)


def get_user_by_access_jti(token: Token, service: AuthServ, auth: Annotated[str, Depends(oauth_scheme)] = None):
    # Tarkistetaan, löytyykö headereistä autorisoitu token
    if not auth:
        raise HTTPException(
            status_code=401,
            detail="Authorization not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Tarkistetaan autentikaatio
    payload = token.verify(auth)
    if payload['type'] != 'access':
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Tarkistetaan access_jti
    user = service.get_user_by_access_jti(payload['sub'])
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # AuthUser
    return user


# LoggedInUser on AuthUser, johon on suoritettu get_user_by_access_jti functio, eli se on autorisoitu käyttäjä.
LoggedInUser = Annotated[AuthUser, Depends(get_user_by_access_jti)]
