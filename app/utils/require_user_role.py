from typing import Annotated
from fastapi import Depends, HTTPException
from app.models import Role
from app.services.roles import RolesServ
from app.utils.logged_in_user import LoggedInUser


def require_manager(service: RolesServ, logged_in_user: LoggedInUser) -> Role:
    user = logged_in_user
    role: Role = service.get_by_id(user.role_id)

    if role.name != "manager":
        raise HTTPException(status_code=403, detail="Unauthorized access")

    return role


def require_employee(service: RolesServ, logged_in_user: LoggedInUser) -> Role:
    user = logged_in_user
    role: Role = service.get_by_id(user.role_id)

    if role.name != "employee":
        raise HTTPException(status_code=403, detail="Unauthorized access")

    return role


RequireManager = Annotated[Role, Depends(require_manager)]
RequireEmployee = Annotated[Role, Depends(require_employee)]