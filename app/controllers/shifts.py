from fastapi import APIRouter
from app.dtos.shifts import UpdateReq, ShiftTime, AddShiftReq, ShiftRes
from app.services.shifts import ShiftsServ
from app.utils.logged_in_user import LoggedInUser

router = APIRouter(
    prefix='/api/shifts',
    tags=['Shifts']
)


# Palauttaa valitun työntekijän kuluvan viikon työvuorot, joiden tyypin
# määrittää shift_type-parametri. Ei käytetä LoggedInUser-mallia, koska
# myös esimiehen on pystyttävä tarkastelemaan alaisensa työvuoroja:
@router.get("/week/{employee_id}/{shift_type}")
def get_shifts_of_week_by_user_id(employee_id: int, shift_type: str, service: ShiftsServ) -> list[ShiftTime]:
    planned_shift_dicts_list = service.get_shifts_by_employee_id(employee_id, shift_type)

    return planned_shift_dicts_list


@router.delete("/{shift_id}")
def delete_shift_by_id(shift_id, service: ShiftsServ):
    service.delete_shift_by_id(shift_id)


@router.patch("/{shift_id}")
def update_shift_by_id(shift_id, updated_shift: UpdateReq, service: ShiftsServ):
    shift = service.update_shift_by_id(shift_id, updated_shift)

    return shift


# Leimaa kirjautuneen työntekijän työvuoron alkaneeksi ja palauttaa leimatun
# vuoron tiedot:
@router.post("/start", status_code=201)
def start_shift(logged_in_user: LoggedInUser, service: ShiftsServ) -> ShiftRes:
    started_shift: ShiftRes = service.start_shift(logged_in_user)
    return started_shift


# Haetaan kirjautuneen työntekijän aloitetun työvuoron tiedot:
@router.get("/started/{employee_id}")
def get_started_shift_by_employee_id(logged_in_user: LoggedInUser, service: ShiftsServ) -> ShiftRes | None:
    return service.get_started_shift(logged_in_user)


# Leimaa valitun työvuoron päättyneeksi ja palauttaa leimatun vuoron tiedot.
@router.patch("/end/{shift_id}")
def end_shift(shift_id: int, logged_in_user: LoggedInUser, service: ShiftsServ) -> ShiftRes:
    ended_shift: ShiftRes = service.end_shift(shift_id, logged_in_user)
    return ended_shift


# Lisää planned-tyyppisen työvuoron halutun työntekijän id:n perusteella, kun
# käyttäjän rooli on manager:
@router.post("/add/{employee_id}", status_code=201)
def add_shift(employee_id: int, service: ShiftsServ, logged_in_user: LoggedInUser, add_shift_req_body: AddShiftReq) -> ShiftRes:
    """Request bodyssa Avain-arvo-parin description-avaimella voi poistaa, jos kuvausta ei haluta lisätä."""
    added_shift: ShiftRes = service.add_shift_by_user_id(employee_id=employee_id,
                                                         logged_in_user=logged_in_user,
                                                         req_body=add_shift_req_body)
    return added_shift



