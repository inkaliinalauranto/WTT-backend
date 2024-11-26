from datetime import datetime, timezone, timedelta
from typing import List
from sqlalchemy import func, cast, Date, or_
from app.custom_exceptions.notfound import NotFoundException
from app.dtos.shifts import ShiftTime, AddShiftReq, ShiftRes
from app.models import Shift, ShiftType, User
from app.services.base_services.shifts_base_service import ShiftsBaseService


class ShiftsServiceSqlAlchemy(ShiftsBaseService):
    def get_shift_by_id(self, shift_id) -> Shift:
        shift = (self.db.query(Shift).filter(Shift.id == shift_id)).first()

        if shift is None:
            raise NotFoundException(message="User not found")

        return shift

    # Haetaan id:n perusteella työntekijän kuluvan viikon työvuorot, jonka
    # tyypin (planned vai confirmed) shift_type-parametri määrittelee:
    def get_shifts_by_employee_id(self, employee_id: int, shift_type: str) -> List[ShiftTime] | None:
        shift_times = (
            self.db.query(Shift.id, func.weekday(Shift.start_time).label("weekday"), ShiftType.type, Shift.start_time,
                          Shift.end_time, Shift.description)
            .join(ShiftType, Shift.shift_type_id == ShiftType.id)
            .join(User, Shift.user_id == User.id)
            .filter(User.id == employee_id,
                    ShiftType.type == shift_type)).all()

        return shift_times

    def delete_shift_by_id(self, shift_id):
        try:
            shift = self.get_shift_by_id(shift_id)
            self.db.delete(shift)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e

    def update_shift_by_id(self, shift_id, updated_shift):
        try:
            shift = self.get_shift_by_id(shift_id)

            # Only update fields in updated_shift that are not None
            for key, value in updated_shift.__dict__.items():
                if value is not None:
                    setattr(shift, key, value)

            # Commit the changes and refresh the shift object
            self.db.commit()
            self.db.refresh(shift)

            return shift

        except Exception as e:
            self.db.rollback()
            raise e

    # Leimataan id:n perusteella valitun käyttäjän työvuoro alkaneeksi:
    def start_shift(self, user: User) -> Shift:
        try:
            shift_type_id = self.db.query(ShiftType.id).filter(ShiftType.type == "confirmed").first()[0]
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')

            shift = Shift(
                start_time=timestamp,
                user_id=user.id,
                shift_type_id=shift_type_id
            )

            self.db.add(shift)
            self.db.commit()
            self.db.refresh(shift)

            return shift

        except Exception as e:
            self.db.rollback()
            raise e

    # Haetaan kirjautuneen työntekijän aloitetun työvuoron tiedot:
    def get_started_shift(self, employee: User) -> Shift | None:
        # HOX! Vaikka editori herjaa, hakuehtoa ei kannata muuttaa muotoon
        # "--Shift.end_time is None--", koska SQLAlchemy ei tunnista näin
        # muotoiltua hakua:
        started_shift = self.db.query(Shift).filter(Shift.user_id == employee.id, Shift.end_time == None).first()
        return started_shift

    # Leimataan id:n perusteella valittu työvuoro päättyneeksi:
    def end_shift(self, shift_id: int) -> Shift:
        try:
            shift = self.get_shift_by_id(shift_id)

            shift.end_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')

            self.db.commit()
            self.db.refresh(shift)

            return shift

        except Exception as e:
            self.db.rollback()
            raise e

    # Lisätään työntekijälle planned-tyyppiä oleva työvuoro. Lisääjän roolin
    # on oltava "manager".
    def add_shift_by_user_id(self, employee_id: int, req_body: AddShiftReq) -> Shift:
        try:
            shift_type_id = self.db.query(ShiftType.id).filter(ShiftType.type == "planned").first()[0]

            shift = Shift(
                start_time=req_body.start_time,
                end_time=req_body.end_time,
                user_id=employee_id,
                shift_type_id=shift_type_id,
                description=req_body.description
            )

            self.db.add(shift)
            self.db.commit()
            self.db.refresh(shift)

            return shift

        except Exception as e:
            self.db.rollback()
            raise e

    # ei käytetä
    def get_shifts_today_by_id(self, employee_id: int) -> List[Shift]:
        today = datetime.now(timezone.utc).date()

        # Tuodaan varalta myös edeltävän ja tulevan päivän data,
        # jos tarvitsee tarkastella vuorokauden vaihdoksella olevia työvuoroja
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        # Käytetään sqlalchemyn cast() funktiota Daten filteröinnissä, jotta huomioidaan vain päivämäärä,
        # koska halutaan hakea kaikki vuorot kyseisenä päivänä riippumatta kellonajasta
        # Tässä on käytetty chatgptä
        shift_list = (self.db.query(Shift)
                      .filter(Shift.user_id == employee_id,
                              or_(cast(Shift.start_time, Date) == yesterday,
                                  cast(Shift.start_time, Date) == today,
                                  cast(Shift.start_time, Date) == tomorrow)
                              ).all())

        # Halutaan palauttaa myös potentiaalisesti tyhjä lista
        return shift_list

    # ei käytetä
    def get_shifts_by_date_by_id(self, employee_id: int, date: datetime) -> List[Shift]:
        # Tänne haetaan päivää edeltävä ja päivää seuraavat datat, jotta vältytään vuorokauden vaihdoksessa
        # olevat ongelmat.
        date = date.date()
        day_after = date + timedelta(days=1)
        day_before = date - timedelta(days=1)

        shift_list = (self.db.query(Shift)
                      .filter(Shift.user_id == employee_id,
                              or_(cast(Shift.start_time, Date) == day_before,
                                  cast(Shift.start_time, Date) == date,
                                  cast(Shift.start_time, Date) == day_after)
                              ).all())

        # Halutaan palauttaa myös potentiaalisesti tyhjä lista
        return shift_list

    def get_shifts_with_days_tolerance_from_today_by_id(self, employee_id: int, days: int) -> List[Shift]:
        # Haetaan 2kuukauden aikaväliltä kaikki työvuorot.
        today = datetime.now(timezone.utc).date()
        month_from_date = today + timedelta(days=days)
        month_past_date = today - timedelta(days=days)

        # Haetaan kaikki työvuorot +- 30päivää tästä päivästä alkaen
        shift_list = (self.db.query(Shift)
                      .filter(Shift.user_id == employee_id,
                              cast(Shift.start_time, Date).between(month_past_date, month_from_date)
                              ).all())

        # Halutaan palauttaa myös potentiaalisesti tyhjä lista
        return shift_list
