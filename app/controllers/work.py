from fastapi import APIRouter
from app.dtos.shifts import UpdateReq, ShiftTime, StartShiftRes, EndShiftRes
from app.services.shifts import ShiftsServ
from app.utils.logged_in_user import LoggedInUser

router = APIRouter(
    prefix='/api/work',
    tags=['Work']
)


# Palauttaa valitun käyttäjän kuluvan viikon työvuorot, joiden tyypin
# määrittää shift_type-parametri. Ei käytetä LoggedInUser-mallia, koska
# myös esimiehen on pystyttävä tarkastelemaan alaisensa työvuoroja:
@router.get("/shifts/week/{user_id}/{shift_type}")
async def get_shifts_of_week_by_user_id(user_id: int, shift_type: str, service: ShiftsServ) -> list[ShiftTime]:
    planned_shift_dicts_list = await service.get_planned_shifts_by_id(user_id, shift_type)

    return planned_shift_dicts_list


@router.delete("/shifts/{shift_id}")
async def delete_shift_by_id(shift_id, service: ShiftsServ):
    await service.delete_shift_by_id(shift_id)


@router.patch("/shifts/{shift_id}")
async def update_shift_by_id(shift_id, updated_shift: UpdateReq, service: ShiftsServ):
    shift = await service.update_shift_by_id(shift_id, updated_shift)

    return shift


# Leimaa kirjautuneen työntekijän työvuoron alkaneeksi ja palauttaa leimatun
# vuoron tiedot:
@router.post("/shifts/start")
async def start_shift(logged_in_user: LoggedInUser, service: ShiftsServ) -> StartShiftRes:
    started_shift = await service.start_shift(logged_in_user)
    return started_shift


# Leimaa valitun työvuoron päättyneeksi ja palauttaa leimatun vuoron tiedot.
# Tässä logged_in_user ei toiminut.
@router.patch("/shifts/end/{shift_id}")
async def end_shift(shift_id: int, service: ShiftsServ) -> EndShiftRes:
    ended_shift = await service.end_shift(shift_id)
    return ended_shift
