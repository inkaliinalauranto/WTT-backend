from typing import Annotated
from fastapi import Depends
from app.custom_exceptions.authorization import UnauthorizedActionException
from app.models import Role, User
from app.dependencies.logged_in_user import LoggedInUser
from app.services.service_factories.roles_serv_factory import RolesServ


def require_manager(service: RolesServ, logged_in_user: LoggedInUser) -> User:
    user = logged_in_user
    role: Role = service.get_by_id(user.role_id)

    if role.name != "manager":
        raise UnauthorizedActionException("Forbidden action")

    return user


def require_employee(service: RolesServ, logged_in_user: LoggedInUser) -> User:
    user = logged_in_user
    role: Role = service.get_by_id(user.role_id)

    if role.name != "employee":
        raise UnauthorizedActionException("Forbidden action")

    return user


RequireManager = Annotated[User, Depends(require_manager)]
RequireEmployee = Annotated[User, Depends(require_employee)]