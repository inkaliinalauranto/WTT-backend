from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import func
from app.db import DB
from app.dtos.shifts import ShiftTime
from app.models import Shift, ShiftType, User


class ShiftsService:
    def __init__(self, db):
        self.db = db

    def get_shift_by_id(self, shift_id):
        """
        SELECT * FROM shifts WHERE shift_id = {shift_id}
        """
        shift = (self.db.query(Shift).filter(Shift.id == shift_id)).first()
        return shift

    # Haetaan id:n perusteella käyttäjän kuluvan viikon suunnitellut työvuorot:
    async def get_planned_shifts_by_id(self, user_id: int) -> list[ShiftTime] | None:
        """
        SELECT s.start_time, s.end_time FROM shifts s
        JOIN shift_types st ON s.shift_type_id = st.id
        JOIN users u ON s.user_id = u.id
        WHERE u.id = {user_id}
        AND st.type = "planned"
        AND YEARWEEK(s.start_time, 1) = YEARWEEK(CURRENT_TIMESTAMP(), 1)
        """

        shift_times = (self.db.query(Shift.start_time, Shift.end_time)
                       .join(ShiftType, Shift.shift_type_id == ShiftType.id)
                       .join(User, Shift.user_id == User.id)
                       .filter(User.id == user_id,
                               ShiftType.type == "planned",
                               func.yearweek(Shift.start_time, 1) == func.yearweek(func.current_timestamp(), 1))).all()

        planned_shift_dicts_list = [ShiftTime(start_time=shift.start_time, end_time=shift.end_time) for shift in
                                    shift_times]

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


def get_service(db: DB):
    return ShiftsService(db)


ShiftsServ = Annotated[ShiftsService, Depends(get_service)]
