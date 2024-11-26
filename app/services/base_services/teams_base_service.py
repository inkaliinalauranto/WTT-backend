import abc


class TeamsBaseService(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, id: int):
        raise NotImplemented()