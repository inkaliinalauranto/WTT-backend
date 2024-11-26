import abc


class OrganizationsBaseService(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, org_id: int):
        raise NotImplemented()