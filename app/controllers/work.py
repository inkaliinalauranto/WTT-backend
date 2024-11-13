from fastapi import APIRouter, HTTPException
from app.services.users import UsersServ

router = APIRouter(
    prefix='/api/work',
    tags=['Work']
)


# Palauttaa valitun käyttäjän kuluvan viikon suunnitellut työvuorot:
@router.get("/shifts/week/{user_id}")
def get_weekly_shifts_by_id(user_id, service: UsersServ):
    planned_shift_dicts_list = service.get_planned_shifts_by_id(user_id)

    if planned_shift_dicts_list is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": service.get_planned_shifts_by_id(user_id)}
