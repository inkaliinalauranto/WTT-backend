from datetime import datetime
from typing import List
from fastapi import APIRouter
from app.dtos.shifts import UpdateReq, ShiftTime, AddShiftReq, ShiftRes
from app.dependencies.logged_in_user import LoggedInUser
from app.dependencies.require_user_role import RequireManager
from app.services.service_factories.shifts_serv_factory import ShiftsServ

router = APIRouter(
    prefix='/api/shifts',
    tags=['Shifts']
)


# Palauttaa valitun työntekijän työvuorot, joiden tyypin määrittää
# shift_type-parametri. Ei käytetä LoggedInUser-mallia, koska
# myös esimiehen on pystyttävä tarkastelemaan alaisensa työvuoroja:
@router.get("/week/{employee_id}/{shift_type}")
def get_all_shifts_by_user_id(employee_id: int, shift_type: str, service: ShiftsServ, logged_in_user: LoggedInUser) -> List[ShiftTime]:
    if logged_in_user:
        shift_times = service.get_shifts_by_employee_id(employee_id, shift_type)

        shift_dicts_list = [ShiftTime(id=shift.id,
                                      shift_type=shift.type,
                                      start_time=shift.start_time,
                                      end_time=shift.end_time,
                                      description=shift.description)
                            for shift in shift_times]

        return shift_dicts_list


@router.delete("/{shift_id}")
def delete_shift_by_id(shift_id, service: ShiftsServ, manager: RequireManager):
    if manager:
        service.delete_shift_by_id(shift_id)


@router.patch("/{shift_id}")
def update_shift_by_id(shift_id, updated_shift: UpdateReq, service: ShiftsServ, manager: RequireManager) -> ShiftRes:
    if manager:
        shift = service.update_shift_by_id(shift_id, updated_shift)
        return ShiftRes.model_validate(shift)


# Leimaa kirjautuneen työntekijän työvuoron alkaneeksi ja palauttaa leimatun
# vuoron tiedot:
@router.post("/start", status_code=201)
def start_shift(logged_in_user: LoggedInUser, service: ShiftsServ) -> ShiftRes:
    started_shift = service.start_shift(logged_in_user)
    return ShiftRes.model_validate(started_shift)


# Haetaan kirjautuneen työntekijän aloitetun työvuoron tiedot:
@router.get("/started")
def get_started_shift_by_employee_id(logged_in_user: LoggedInUser, service: ShiftsServ) -> ShiftRes | None:
    started_shift = service.get_started_shift(logged_in_user)

    if started_shift is None:
        return None

    return ShiftRes.model_validate(started_shift)


# Leimaa valitun työvuoron päättyneeksi ja palauttaa leimatun vuoron tiedot.
@router.patch("/end/{shift_id}")
def end_shift(shift_id: int, logged_in_user: LoggedInUser, service: ShiftsServ) -> ShiftRes:
    if logged_in_user is not None:
        ended_shift = service.end_shift(shift_id)
        return ShiftRes.model_validate(ended_shift)


# Lisää planned-tyyppisen työvuoron halutun työntekijän id:n perusteella, kun
# käyttäjän rooli on manager:
@router.post("/add/{employee_id}", status_code=201)
def add_shift(employee_id: int, service: ShiftsServ, manager: RequireManager, add_shift_req_body: AddShiftReq) -> ShiftRes:
    if manager is not None:
        """Request bodyssa Avain-arvo-parin description-avaimella voi poistaa, jos kuvausta ei haluta lisätä."""
        added_shift = service.add_shift_by_user_id(employee_id, add_shift_req_body)
        return ShiftRes.model_validate(added_shift)


@router.get("/today/{employee_id}")
def get_shifts_today_by_employee_id(employee_id: int, service: ShiftsServ, user:LoggedInUser) -> list[ShiftRes]:
    if user is not None:
        shift_list = service.get_shifts_today_by_id(employee_id)
        shifts = []
        for shift in shift_list:
            shifts.append(ShiftRes.model_validate(shift))
        return shifts


@router.get("/{date}/{employee_id}")
def get_shifts_today_by_employee_id(employee_id: int, date: datetime, service: ShiftsServ, user:LoggedInUser) -> list[ShiftRes]:
    if user is not None:
        shift_list = service.get_shifts_by_date_by_id(employee_id, date)
        shifts = []
        for shift in shift_list:
            shifts.append(ShiftRes.model_validate(shift))
        return shifts


# Haetaan kaikki työvuorot +- days päivää from today päivästä lähtien.
@router.get("/today/{employee_id}/tolerance/{days}")
def get_shifts_with_days_tolerance_from_today_by_employee_id(employee_id: int, days: int, service: ShiftsServ, user:LoggedInUser) -> list[ShiftRes]:
    if user is not None:
        shift_list = service.get_shifts_with_days_tolerance_from_today_by_id(employee_id, days)
        shifts = []
        for shift in shift_list:
            shifts.append(ShiftRes.model_validate(shift))
        return shifts