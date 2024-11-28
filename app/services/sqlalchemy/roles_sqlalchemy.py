from app.custom_exceptions.notfound import NotFoundException
from app.custom_exceptions.taken import TakenException
from app.models import Role
from app.services.base_services.roles_base_service import RolesBaseService


class RolesServiceSqlalchemy(RolesBaseService):
    # Haetaan käyttäjä id:n perusteella:
    def get_by_id(self, role_id) -> Role:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if role is None:
            raise NotFoundException("Role not found")
        return role


    # Haetaan nimen perusteella
    def get_by_name(self, role_name) -> Role:
        role = self.db.query(Role).filter(Role.name == role_name).first()
        if role is None:
            raise NotFoundException("Role not found")
        return role


    def create_role_if_not_exist(self, role_name: str) -> Role:
        try:
            role = self.db.query(Role).filter(Role.name == role_name).first()
            if role is None:
                new_role = Role(name=role_name)
                self.db.add(new_role)
                self.db.commit()
                self.db.refresh(new_role)
                return new_role

            raise TakenException("Role already exists")

        except Exception as e:
            self.db.rollback()
            raise e