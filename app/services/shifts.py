from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import func, insert, cast, Date, or_
from app.db import DB
from app.dtos.shifts import ShiftTime, AddShiftReq, ShiftRes
from app.models import Shift, ShiftType, User, Role


class ShiftsService:
    def __init__(self, db):
        self.db = db

    def get_shift_by_id(self, shift_id):
        """
        SELECT * FROM shifts WHERE shift_id = {shift_id}
        """
        shift = (self.db.query(Shift).filter(Shift.id == shift_id)).first()
        return shift

    # Haetaan id:n perusteella työntekijän kuluvan viikon työvuorot, jonka
    # tyypin (planned vai confirmed) shift_type-parametri määrittelee:
    def get_shifts_by_employee_id(self, employee_id: int, shift_type: str) -> list[ShiftTime] | None:
        shift_times = (
            self.db.query(Shift.id, func.weekday(Shift.start_time).label("weekday"), ShiftType.type, Shift.start_time,
                          Shift.end_time, Shift.description)
            .join(ShiftType, Shift.shift_type_id == ShiftType.id)
            .join(User, Shift.user_id == User.id)
            .filter(User.id == employee_id,
                    ShiftType.type == shift_type)).all()

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        shift_dicts_list = [ShiftTime(id=shift.id,
                                      weekday=weekdays[shift.weekday],
                                      shift_type=shift.type,
                                      start_time=shift.start_time,
                                      end_time=shift.end_time,
                                      description=shift.description)
                            for shift in shift_times]

        return shift_dicts_list

    def delete_shift_by_id(self, shift_id):
        try:
            shift = self.get_shift_by_id(shift_id)

            if shift is None:
                raise HTTPException(status_code=404, detail="Shift not found")

            self.db.delete(shift)

            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e

    def update_shift_by_id(self, shift_id, updated_shift):
        try:
            shift = self.get_shift_by_id(shift_id)

            if shift is None:
                raise HTTPException(status_code=404, detail="Shift not found")

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
    def start_shift(self, user: User) -> ShiftRes:
        try:
            shift_type_id = self.db.query(ShiftType.id).filter(ShiftType.type == "confirmed").first()[0]
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')

            add_query = insert(Shift).values(start_time=timestamp,
                                             user_id=user.id,
                                             shift_type_id=shift_type_id)

            result = self.db.execute(add_query)
            shift_id = result.lastrowid
            self.db.commit()

            return ShiftRes(id=shift_id,
                            start_time=timestamp,
                            end_time=None,
                            user_id=user.id,
                            shift_type_id=shift_type_id,
                            description=None)

        except Exception as e:
            self.db.rollback()
            raise e

    # Haetaan kirjautuneen työntekijän aloitetun työvuoron tiedot:
    def get_started_shift(self, employee: User) -> ShiftRes | None:
        # HOX! Vaikka editori herjaa, hakuehtoa ei kannata muuttaa muotoon
        # "--Shift.end_time is None--", koska SQLAlchemy ei tunnista näin
        # muotoiltua hakua:
        started_shift = self.db.query(Shift).filter(Shift.user_id == employee.id, Shift.end_time == None).first()

        if started_shift is not None:
            started_shift = ShiftRes(id=started_shift.id,
                                     start_time=started_shift.start_time,
                                     end_time=started_shift.end_time,
                                     user_id=started_shift.user_id,
                                     shift_type_id=started_shift.shift_type_id,
                                     description=started_shift.description)

        return started_shift

    # Leimataan id:n perusteella valittu työvuoro päättyneeksi:
    def end_shift(self, shift_id: int, user: User) -> ShiftRes:
        try:
            shift = self.get_shift_by_id(shift_id)

            if shift.user_id != user.id:
                raise HTTPException(status_code=401, detail="Unauthorized action")

            shift.end_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')

            self.db.commit()

            return ShiftRes(id=shift.id,
                            start_time=shift.start_time,
                            end_time=shift.end_time,
                            user_id=shift.user_id,
                            shift_type_id=shift.shift_type_id,
                            description=shift.description)

        except Exception as e:
            self.db.rollback()
            raise e

    # Lisätään työntekijälle planned-tyyppiä oleva työvuoro. Lisääjän roolin
    # on oltava "manager".
    def add_shift_by_user_id(self, employee_id: int, req_body: AddShiftReq) -> ShiftRes:
        try:
            shift_type_id = self.db.query(ShiftType.id).filter(ShiftType.type == "planned").first()[0]

            add_query = insert(Shift).values(start_time=req_body.start_time,
                                             end_time=req_body.end_time,
                                             user_id=employee_id,
                                             shift_type_id=shift_type_id,
                                             description=req_body.description)

            result = self.db.execute(add_query)
            shift_id = result.lastrowid
            self.db.commit()

            return ShiftRes(id=shift_id,
                            start_time=req_body.start_time,
                            end_time=req_body.end_time,
                            user_id=employee_id,
                            shift_type_id=shift_type_id,
                            description=req_body.description)

        except Exception as e:
            self.db.rollback()
            raise e


    def get_shifts_today_by_id(self, employee_id: int) -> list[ShiftRes]:
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

        # Täältä palautetaan vain data. Listat järjestellään muualla
        shifts: list[ShiftRes] = []
        for shift in shift_list:
            shifts.append(ShiftRes.model_validate(shift))


        # Halutaan palauttaa myös potentiaalisesti tyhjä lista
        return shifts


    def get_shifts_by_date_by_id(self, employee_id: int, date: datetime) -> list[ShiftRes]:
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

        # Täältä palautetaan vain data. Listat järjestellään muualla
        shifts: list[ShiftRes] = []
        for shift in shift_list:
            shifts.append(ShiftRes.model_validate(shift))

        # Halutaan palauttaa myös potentiaalisesti tyhjä lista
        return shifts


    def get_shifts_with_days_tolerance_from_today_by_id(self, employee_id: int, days: int) -> list[ShiftRes]:
        # Haetaan 2kuukauden aikaväliltä kaikki työvuorot.
        today = datetime.now(timezone.utc).date()
        month_from_date = today + timedelta(days=days)
        month_past_date = today - timedelta(days=days)

        # Haetaan kaikki työvuorot +- 30päivää tästä päivästä alkaen
        shift_list = (self.db.query(Shift)
                      .filter(Shift.user_id == employee_id,
                              cast(Shift.start_time, Date).between(month_past_date, month_from_date)
                              ).all())

        # Täältä palautetaan vain data. Listat järjestellään muualla
        shifts: list[ShiftRes] = []
        for shift in shift_list:
            shifts.append(ShiftRes.model_validate(shift))

        # Halutaan palauttaa myös potentiaalisesti tyhjä lista
        return shifts


def get_service(db: DB):
    return ShiftsService(db)


ShiftsServ = Annotated[ShiftsService, Depends(get_service)]
