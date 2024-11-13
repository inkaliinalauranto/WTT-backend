from fastapi import APIRouter, HTTPException
from app.dtos.users import ShiftTime
from app.services.users import UsersServ

router = APIRouter(
    prefix='/api/work',
    tags=['Work']
)


# Palauttaa valitun käyttäjän kuluvan viikon suunnitellut työvuorot:
@router.get("/shifts/week/{user_id}")
async def get_weekly_shifts_by_id(user_id: int, service: UsersServ) -> list[ShiftTime]:
    planned_shift_dicts_list = await service.get_planned_shifts_by_id(user_id)

    if planned_shift_dicts_list is None:
        raise HTTPException(status_code=404, detail="User not found")

    return planned_shift_dicts_list
