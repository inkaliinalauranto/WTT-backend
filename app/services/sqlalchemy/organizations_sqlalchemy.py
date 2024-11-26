from app.custom_exceptions.notfound import NotFoundException
from app.db_mysql import DB
from app.models import Organization
from app.services.base_services.organizations_base_service import OrganizationsBaseService


class OrganizationsServiceSqlAlchemy(OrganizationsBaseService):
    def __init__(self, db: DB):
        self.db = db

    def get_by_id(self, org_id) -> Organization:
        organization = self.db.query(Organization).filter(Organization.id == org_id).first()
        if organization is None:
            raise NotFoundException("Organization not found")
        return organization