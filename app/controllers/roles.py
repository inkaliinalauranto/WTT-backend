from fastapi import APIRouter
from app.dtos.roles import Role
from app.services.roles import RolesServ


router = APIRouter(
    prefix='/api/roles',
    tags=['Roles']
)


@router.get("/{role_id}")
async def get_role_by_id(role_id: int, service: RolesServ) -> Role:
    role = service.get_by_id(role_id)
    return role
