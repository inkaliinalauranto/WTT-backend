import abc
from app.models import User
from app.services.base_services.base_service import BaseService


class UsersBaseService(abc.ABC, BaseService):
    @abc.abstractmethod
    def get_by_id(self, user_id: int):
        raise NotImplemented()
    
    @abc.abstractmethod
    def get_all_by_team_id(self, team_id:int):
        raise NotImplemented()
    
    @abc.abstractmethod
    def create(self, user: User):
        raise NotImplemented()
    
    @abc.abstractmethod
    def get_user_by_access_jti(self, access_jti):
        raise NotImplemented()
    
    @abc.abstractmethod
    def delete_user_by_id(self, user_id: int, manager:User):
        raise NotImplemented()