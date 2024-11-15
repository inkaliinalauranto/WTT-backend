from fastapi import APIRouter
from app.services.users import UsersServ

router = APIRouter(
    prefix='/api/users',
    tags=['Users']
)

@router.delete("/{user_id}", status_code=204)
async def delete_user_by_id(user_id, service: UsersServ):
    await service.delete_user_by_id(user_id)