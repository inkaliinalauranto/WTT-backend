from app.custom_exceptions.notfound import NotFoundException
from app.models import Role
from app.services.base_services.roles_base_service import RolesBaseService


class RolesServiceSqlalchemy(RolesBaseService):
    # Haetaan käyttäjä id:n perusteella:
    def get_by_id(self, role_id) -> Role:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if role is None:
            raise NotFoundException("Role not found")
        return role
