import abc
from app.services.base_services.base_service import BaseService


class TeamsBaseService(abc.ABC, BaseService):
    @abc.abstractmethod
    def get_by_id(self, team_id: int):
        raise NotImplemented()