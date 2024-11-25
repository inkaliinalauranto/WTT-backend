from typing import Annotated
from fastapi import Depends, HTTPException
from app.models import Role, User
from app.services.roles import RolesServ
from app.dependencies.logged_in_user import LoggedInUser


def require_manager(service: RolesServ, logged_in_user: LoggedInUser) -> User:
    user = logged_in_user
    role: Role = service.get_by_id(user.role_id)

    if role.name != "manager":
        raise HTTPException(status_code=403, detail="Forbidden action")

    return user


def require_employee(service: RolesServ, logged_in_user: LoggedInUser) -> User:
    user = logged_in_user
    role: Role = service.get_by_id(user.role_id)

    if role.name != "employee":
        raise HTTPException(status_code=403, detail="Forbidden action")

    return user


RequireManager = Annotated[User, Depends(require_manager)]
RequireEmployee = Annotated[User, Depends(require_employee)]