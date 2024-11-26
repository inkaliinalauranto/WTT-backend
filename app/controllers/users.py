from fastapi import APIRouter
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
        return service.get_all_by_team_id(manager.team_id)
