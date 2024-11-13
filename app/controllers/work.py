from fastapi import APIRouter, HTTPException
from app.dtos.shifts import UpdateReq
from app.services.users import UsersServ
from app.services.shifts import ShiftsServ

router = APIRouter(
    prefix='/api/work',
    tags=['Work']
)


# Palauttaa valitun käyttäjän kuluvan viikon suunnitellut työvuorot:
@router.get("/shifts/week/{user_id}")
async def get_weekly_shifts_by_id(user_id, service: UsersServ):
    planned_shift_dicts_list = service.get_planned_shifts_by_id(user_id)

    if planned_shift_dicts_list is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": service.get_planned_shifts_by_id(user_id)}

@router.delete("/shifts/{shift_id}")
async def delete_shift_by_id(shift_id, service: ShiftsServ):
    service.delete_shift_by_id(shift_id)

@router.patch("/shifts/{shift_id}")
async def update_shift_by_id(shift_id, updated_shift: UpdateReq, service: ShiftsServ):
    shift = service.update_shift_by_id(shift_id, updated_shift)

    return shift