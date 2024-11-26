import abc
from app.services.base_services.base_service import BaseService


class OrganizationsBaseService(abc.ABC, BaseService):
    @abc.abstractmethod
    def get_by_id(self, org_id: int):
        raise NotImplemented()