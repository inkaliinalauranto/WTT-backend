from datetime import datetime
from pydantic import BaseModel


class UpdateReq(BaseModel):
    start_time: datetime
    end_time: datetime 
    user_id: int
    shift_type_id: int
    description: str