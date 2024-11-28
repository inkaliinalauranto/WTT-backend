from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app import models
from app.custom_exceptions.notfound import NotFoundException
from app.custom_exceptions.taken import TakenException
from app.dependencies.logged_in_user import LoggedInUser
from app.dependencies.require_user_role import RequireManager, RequireAdmin
from app.services.service_factories.auth_serv_factory import AuthServ
from app.services.service_factories.organizations_serv_factory import OrganizationsServ
from app.services.service_factories.roles_serv_factory import RolesServ
from app.services.service_factories.teams_serv_factory import TeamsServ
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


# Luo tietokantaan uusi työntekijä. Manager endpoint
@router.post("/register/employee", status_code=201)
async def create_new_employee(
        req: RegisterReq, users_service: UsersServ, roles_service: RolesServ, manager: RequireManager
) -> AuthUser:
    if manager is not None:
        # Luodaan requestista vajaa models.User instanssi. Service täyttää loput.
        user = models.User(**req.model_dump())

        # Ylikirjoitetaan annettu rooli employeeksi
        employee_role = roles_service.get_by_name("employee")
        if employee_role is None:
                employee_role = roles_service.create_role_if_not_exist("employee")

        user.role_id = employee_role.id
        users_service.create(user, creator_role_id=manager.role_id)

        return AuthUser.model_validate(user)


# Luo tietokantaan mikä tahansa käyttäjä. Admin endpoint
@router.post("/register/user", status_code=201)
async def create_new_user(req: RegisterReq, users_service: UsersServ, roles_service: RolesServ, admin: RequireAdmin) -> AuthUser:
    if admin is not None:
        user = models.User(**req.model_dump())
        if req.role_id is None:
            raise NotFoundException("Request body does not contain role id")

        if roles_service.get_by_id(req.role_id) is None:
            raise NotFoundException("Role not found")

        users_service.create(user, creator_role_id=admin.role_id)
        return AuthUser.model_validate(user)


# Luodaan tietokantaan admin. Admineita voidaan luoda vain yksi
@router.post("/register/admin", status_code=201)
async def create_admin_if_not_exist(
        user_service: UsersServ, roles_service: RolesServ, teams_service: TeamsServ, orgs_service: OrganizationsServ
) -> str:
    # Luodaan adminrole. Mikäli se on jo luotu, tulee TakenExpection, ja adminia ei luoda uudelleen.
    # Exception pitää huolen, ettei toista adminia luoda
    try:
        admin_role = roles_service.create_role_if_not_exist("admin")
        admin_org = orgs_service.create_org_if_not_exist("admin")
        admin_team = teams_service.create_team_if_not_exist("admin", admin_org.id)
    except TakenException:
        # Vaihdetaan viesti, jos admin on jo luotu
        raise TakenException("Admin already exists")

    # Luodaan admin käyttäjä, mikäli adminia ei ollut vielä olemassa.
    user_service.create_admin(admin_role, admin_team)

    return "Admin created"


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
