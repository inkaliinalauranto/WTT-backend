from typing import List
from fastapi import APIRouter

from app.dependencies.logged_in_user import LoggedInUser
from app.dtos.auth import AuthUser
from app.services.service_factories.users_serv_factory import UsersServ
from app.dependencies.require_user_role import RequireManager


router = APIRouter(
    prefix='/api/users',
    tags=['Users']
)


@router.delete("/{user_id}", status_code=204)
def delete_user_by_id(user_id, service: UsersServ, manager: RequireManager):
    if manager is not None:
        service.delete_user_by_id(user_id, manager)


@router.get("/manager/{team_id}")
async def get_all_employees_by_manager_team_id(service: UsersServ, manager: RequireManager) -> list[AuthUser]:
    if manager is not None:
        users = service.get_all_by_team_id(manager.team_id)
        users_list: List[AuthUser] = []
        for user in users:
            users_list.append(AuthUser.model_validate(user))
        return users_list


@router.post("/is-working/{boolean}")
def set_user_working_status(boolean: bool, service: UsersServ, user: LoggedInUser) -> None:
    if user is not None:
        service.set_working_status_by_id(user, boolean)
