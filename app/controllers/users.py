from fastapi import APIRouter
from app.services.users import UsersServ
from app.utils.require_user_role import RequireManager

router = APIRouter(
    prefix='/api/users',
    tags=['Users']
)


@router.delete("/{user_id}", status_code=204)
def delete_user_by_id(user_id, service: UsersServ, require_manager: RequireManager):
    role = require_manager
    service.delete_user_by_id(user_id, role)