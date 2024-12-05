import abc
from app.services.base_services.base_service import BaseService


class OrganizationsBaseService(abc.ABC, BaseService):
    @abc.abstractmethod
    def get_by_id(self, org_id: int):
        raise NotImplemented()

    @abc.abstractmethod
    def create_org_if_not_exist(self, org_name: str):
        raise NotImplemented()

    @abc.abstractmethod
    def delete_all(self):
        raise NotImplemented()

