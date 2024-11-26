import abc


class OrganizationsBaseService(abc.ABC):
    @abs.abstractmethod
    def get_by_id(self, org_id: int):
        raise NotImplemented()