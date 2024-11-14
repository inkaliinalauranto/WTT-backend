from fastapi import APIRouter, HTTPException
from app.dtos.shifts import UpdateReq, ShiftTime, StartShiftRes, EndShiftRes
from app.services.shifts import ShiftsServ

router = APIRouter(
    prefix='/api/work',
    tags=['Work']
)


# Palauttaa valitun käyttäjän kuluvan viikon suunnitellut työvuorot:
@router.get("/shifts/week/{user_id}")
async def get_weekly_shifts_by_id(user_id: int, service: ShiftsServ) -> list[ShiftTime]:
    planned_shift_dicts_list = await service.get_planned_shifts_by_id(user_id)

    return planned_shift_dicts_list


@router.delete("/shifts/{shift_id}")
async def delete_shift_by_id(shift_id, service: ShiftsServ):
    service.delete_shift_by_id(shift_id)


@router.patch("/shifts/{shift_id}")
async def update_shift_by_id(shift_id, updated_shift: UpdateReq, service: ShiftsServ):
    shift = service.update_shift_by_id(shift_id, updated_shift)

    return shift


# Leimaa valitun työntekijän työvuoron alkaneeksi ja palauttaa leimatun vuoron
# tiedot:
@router.post("/shifts/start/{user_id}")
async def start_shift(user_id: int, service: ShiftsServ) -> StartShiftRes:
    started_shift = await service.start_shift(user_id)
    return started_shift


# Leimaa valitun työntekijän työvuoron päättyneeksi ja palauttaa leimatun
# vuoron tiedot:
@router.patch("/shifts/end/{shift_id}")
async def end_shift(shift_id: int, service: ShiftsServ) -> EndShiftRes:
    ended_shift = await service.end_shift(shift_id)
    return ended_shift
