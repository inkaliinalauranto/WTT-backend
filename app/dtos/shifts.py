from datetime import datetime
from pydantic import BaseModel


class EndShiftRes(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    user_id: int
    shift_type_id: int


class StartShiftRes(BaseModel):
    id: int
    start_time: datetime
    user_id: int
    shift_type_id: int


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
