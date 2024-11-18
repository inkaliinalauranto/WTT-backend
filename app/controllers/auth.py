from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app import models
from app.utils.logged_in_user import LoggedInUser
from app.utils.access_token import Token
from fastapi import APIRouter, Depends
from app.dtos.auth import LoginRes, AuthUser, LoginReq, RegisterReq
from app.services.users import UsersServ
from app.services.auth import AuthServ


# MVC mallin mukaisesti tänne tulee vain requestin vastaanotto ja controlleri palauttaa responsen.
# Näissä ei tarvitse injektoida tietokantayhteyttä, koska se injektoidaan jo kun Repo tai Service annetaan parametrinä
# controllerille.


router = APIRouter(
    prefix='/api/auth',
    tags=['Authorization']
)


# Apufunktio nopeuttamaan userin mäppäystä auth useriksi.
def map_to_auth_user(user: models.User):
    return AuthUser(id=user.id, username=user.username, role_id=user.role_id, team_id=user.team_id)


# Hae logged in user, vaatii kirjautuneen käyttäjän riippuvuutena.
# LoggedInUser hakee käyttäjän access_jti:n perusteella ja palauttaa AuthUserin.
@router.get("/user")
async def get_logged_in_user(logged_in_user: LoggedInUser) -> AuthUser:
    user = logged_in_user
    return map_to_auth_user(user)


# Luo tietokantaan uusi käyttäjä. 201 = Created
@router.post("/register", status_code=201)
async def create_new_user(req: RegisterReq, service: UsersServ) -> AuthUser:
    # Luodaan requestista vajaa models.User instanssi. Service täyttää loput.
    user = models.User(**req.model_dump())
    service.create(user)
    return map_to_auth_user(user)


# Login openapin docsin kaavakkeella
@router.post("/login/openapi")
async def login_openapi(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthServ, token: Token
) -> LoginRes:
    # Loginissa luodaan AuthUser ja Token, jotka palautetaan function suoriuduttua.
    user, access_token = service.login(form_data, token)
    return LoginRes(access_token=access_token, auth_user=map_to_auth_user(user))


# Normaali login request
@router.post("/login")
async def login(req: LoginReq, service: AuthServ, token: Token) -> LoginRes:
    # Loginissa luodaan AuthUser ja Token, jotka palautetaan function suoriuduttua.
    user, access_token = service.login(req, token)

    res = LoginRes(access_token=access_token, auth_user=map_to_auth_user(user))
    res.set_cookie("wtt-cookie", access_token, httponly=True, secure=True)

    return res


# Poistetaan jti tietokannasta uloskirjautuessa. Vaatii tokenin. 204 = No content
@router.post("/logout", status_code=204)
async def logout(logged_in_user: LoggedInUser, service: AuthServ):
    service.logout(logged_in_user)
