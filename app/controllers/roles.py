from fastapi import APIRouter

from app import models
from app.dtos.roles import Role
from app.services.service_factories.roles_serv_factory import RolesServ



router = APIRouter(
    prefix='/api/roles',
    tags=['Roles']
)


@router.get("/{role_id}")
async def get_role_by_id(role_id: int, service: RolesServ) -> Role:
    role: models.Role = service.get_by_id(role_id)
    return Role.model_validate(role)
