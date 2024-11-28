import abc
from app.models import User, Role, Team
from app.services.base_services.base_service import BaseService


class UsersBaseService(abc.ABC, BaseService):
    @abc.abstractmethod
    def get_by_id(self, user_id: int):
        raise NotImplemented()
    
    @abc.abstractmethod
    def get_all_by_team_id(self, team_id:int):
        raise NotImplemented()
    
    @abc.abstractmethod
    def create(self, user: User, creator_role_id: int):
        raise NotImplemented()
    
    @abc.abstractmethod
    def get_user_by_access_jti(self, access_jti):
        raise NotImplemented()
    
    @abc.abstractmethod
    def delete_user_by_id(self, user_id: int, manager:User):
        raise NotImplemented()

    @abc.abstractmethod
    def set_working_status_by_id(self, user, is_working):
        raise NotImplemented()

    @abc.abstractmethod
    def create_admin(self, admin_role: Role, admin_team: Team):
        raise NotImplemented()