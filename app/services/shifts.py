from datetime import datetime
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import func, insert
from app.db import DB
from app.dtos.shifts import ShiftTime, StartShiftRes, EndShiftRes
from app.models import Shift, ShiftType, User
from app.utils.logged_in_user import LoggedInUser


class ShiftsService:
    def __init__(self, db):
        self.db = db

    def get_shift_by_id(self, shift_id):
        """
        SELECT * FROM shifts WHERE shift_id = {shift_id}
        """
        shift = (self.db.query(Shift).filter(Shift.id == shift_id)).first()
        return shift

    # Haetaan id:n perusteella käyttäjän kuluvan viikon työvuorot, jonka
    # tyypin (planned vai confirmed) shift_type-parametri määrittelee:
    def get_shifts_by_user_id(self, user_id: int, shift_type: str) -> list[ShiftTime] | None:
        shift_times = (
            self.db.query(Shift.id, func.weekday(Shift.start_time).label("weekday"), ShiftType.type, Shift.start_time, Shift.end_time)
            .join(ShiftType, Shift.shift_type_id == ShiftType.id)
            .join(User, Shift.user_id == User.id)
            .filter(User.id == user_id,
                    ShiftType.type == shift_type,
                    func.yearweek(Shift.start_time, 1) == func.yearweek(func.current_timestamp(), 1))).all()

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        planned_shift_dicts_list = [ShiftTime(id=shift.id,
                                              weekday=weekdays[shift.weekday],
                                              shift_type=shift.type,
                                              start_time=shift.start_time,
                                              end_time=shift.end_time)
                                    for shift in shift_times]

        return planned_shift_dicts_list

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
    def start_shift(self, logged_in_user: LoggedInUser) -> StartShiftRes:
        try:
            shift_type_id = self.db.query(ShiftType.id).filter(ShiftType.type == "confirmed").first()[0]

            add_query = insert(Shift).values(start_time=func.current_timestamp(),
                                             user_id=logged_in_user.id,
                                             shift_type_id=shift_type_id)

            result = self.db.execute(add_query)
            shift_id = result.lastrowid
            self.db.commit()

            return StartShiftRes(id=shift_id,
                                 start_time=datetime.now().replace(microsecond=0),
                                 user_id=logged_in_user.id,
                                 shift_type_id=shift_type_id)

        except Exception as e:
            self.db.rollback()
            raise e

    # Leimataan id:n perusteella valittu työvuoro päättyneeksi:
    def end_shift(self, shift_id: int) -> EndShiftRes:
        try:
            shift = self.get_shift_by_id(shift_id)
            shift.end_time = func.current_timestamp()

            self.db.commit()

            return EndShiftRes(id=shift.id,
                               start_time=shift.start_time,
                               end_time=datetime.now().replace(microsecond=0),
                               user_id=shift.user_id,
                               shift_type_id=shift.shift_type_id)

        except Exception as e:
            self.db.rollback()
            raise e


def get_service(db: DB):
    return ShiftsService(db)


ShiftsServ = Annotated[ShiftsService, Depends(get_service)]
