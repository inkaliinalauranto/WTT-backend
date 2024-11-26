from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app import models
from app.dependencies.logged_in_user import LoggedInUser
from app.services.service_factories.auth_serv_factory import AuthServ
from app.utils.access_token import Token
from fastapi import APIRouter, Depends, Response
from app.dtos.auth import LoginRes, AuthUser, LoginReq, RegisterReq
from app.services.service_factories.users_serv_factory import UsersServ


# MVC mallin mukaisesti tänne tulee vain requestin vastaanotto ja controlleri palauttaa responsen.
# Näissä ei tarvitse injektoida tietokantayhteyttä, koska se injektoidaan jo kun Repo tai Service annetaan parametrinä
# controllerille.


router = APIRouter(
    prefix='/api/auth',
    tags=['Authorization']
)


# Hae logged in user, vaatii kirjautuneen käyttäjän riippuvuutena.
# LoggedInUser hakee käyttäjän access_jti:n perusteella ja palauttaa AuthUserin.
@router.get("/user")
async def get_logged_in_user(user: LoggedInUser) -> AuthUser:
    return AuthUser.model_validate(user)


# Luo tietokantaan uusi käyttäjä. 201 = Created
@router.post("/register", status_code=201)
async def create_new_user(req: RegisterReq, service: UsersServ) -> AuthUser:
    # Luodaan requestista vajaa models.User instanssi. Service täyttää loput.
    user = models.User(**req.model_dump())
    service.create(user)
    return AuthUser.model_validate(user)


# Login openapin docsin kaavakkeella
@router.post("/login/openapi")
async def login_openapi(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthServ, token: Token, response: Response
) -> LoginRes:
    user, access_token = service.login(form_data, token)

    # Asetetaan responseen cookie mukaan, jottei sitä tarvitse tehdä frontissa.
    # Matiakselta saatu ohje
    response.set_cookie(key="wtt-cookie", value=access_token, httponly=True, secure=True)

    # Loginissa luodaan User ja Token, jotka palautetaan. User mäpätään AuthUseriksi, joka on response dto.
    return LoginRes(access_token=access_token, auth_user=AuthUser.model_validate(user))


# Normaali login request
@router.post("/login")
async def login(req_data: LoginReq, service: AuthServ, token: Token, response: Response) -> LoginRes:
    user, access_token = service.login(req_data, token)
    response.set_cookie("wtt-cookie", access_token, httponly=True, secure=True)
    return LoginRes(access_token=access_token, auth_user=AuthUser.model_validate(user))


# Poistetaan jti tietokannasta uloskirjautuessa ja cookie selaimesta. Vaatii tokenin. 204 = No content
@router.post("/logout", status_code=204)
async def logout(user: LoggedInUser, service: AuthServ, response: Response):
    response.delete_cookie(key="wtt-cookie", httponly=True, secure=True)
    service.logout(user)
