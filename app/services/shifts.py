from typing import Annotated

from fastapi import Depends, HTTPException

from app.db import DB
from app.models import Shift


class ShiftsService:
    def __init__(self, db):
        self.db = db

    def get_shift_by_id(self, shift_id):
        """
        SELECT * FROM shifts WHERE shift_id = {shift_id}
        """
        shift = (self.db.query(Shift).filter(Shift.id == shift_id)).first()
        return shift
    
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