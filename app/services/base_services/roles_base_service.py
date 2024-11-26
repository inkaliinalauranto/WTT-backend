import abc
from app.services.base_services.base_service import BaseService


class RolesBaseService(abc.ABC, BaseService):
    @abc.abstractmethod
    def get_by_id(self, role_id: int):
        raise NotImplemented()
