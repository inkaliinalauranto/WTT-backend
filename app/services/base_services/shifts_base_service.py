import abc
from datetime import datetime
from typing import List

from app.dtos.shifts import ShiftTime, ShiftRes, AddShiftReq
from app.models import User


class ShiftsBaseService(abc.ABC):
    @abc.abstractmethod
    def get_shift_by_id(self, shift_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_shifts_by_employee_id(self, employee_id: int, shift_type: str) -> List[ShiftTime] | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_shift_by_id(self, shift_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def update_shift_by_id(self, shift_id, updated_shift):
        raise NotImplementedError()

    @abc.abstractmethod
    def start_shift(self, user: User) -> ShiftRes:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_started_shift(self, employee: User) -> ShiftRes | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def end_shift(self, shift_id: int, user: User) -> ShiftRes:
        raise NotImplementedError()

    @abc.abstractmethod
    def add_shift_by_user_id(self, employee_id: int, req_body: AddShiftReq) -> ShiftRes:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_shifts_today_by_id(self, employee_id: int) -> List[ShiftRes]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_shifts_by_date_by_id(self, employee_id: int, date: datetime) -> List[ShiftRes]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_shifts_with_days_tolerance_from_today_by_id(self, employee_id: int, days: int) -> List[ShiftRes]:
        raise NotImplementedError()
