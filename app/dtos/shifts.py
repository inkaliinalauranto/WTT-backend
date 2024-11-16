from datetime import datetime
from pydantic import BaseModel


class ShiftRes(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime | None
    user_id: int
    shift_type_id: int
    description: str | None


class ShiftTime(BaseModel):
    id: int
    weekday: str
    shift_type: str
    start_time: datetime
    end_time: datetime | None


class UpdateReq(BaseModel):
    start_time: datetime
    end_time: datetime
    user_id: int
    shift_type_id: int
    description: str


class AddShiftReq(BaseModel):
    start_time: datetime
    end_time: datetime
    description: str | None = None
