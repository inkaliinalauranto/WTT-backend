from app.custom_exceptions.notfound import NotFoundException
from app.custom_exceptions.taken import TakenException
from app.models import Organization
from app.services.base_services.organizations_base_service import OrganizationsBaseService


class OrganizationsServiceSqlAlchemy(OrganizationsBaseService):
    def get_by_id(self, org_id) -> Organization:
        organization = self.db.query(Organization).filter(Organization.id == org_id).first()
        if organization is None:
            raise NotFoundException("Organization not found")
        return organization

    def create_org_if_not_exist(self, org_name: str) -> Organization:
        try:
            org = self.db.query(Organization).filter(Organization.name == org_name).first()
            if org is None:
                new_org = Organization(name=org_name)
                self.db.add(new_org)
                self.db.commit()
                self.db.refresh(new_org)
                return new_org

            raise TakenException("Organization already exists")

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_all(self):
        organizations = self.db.query(Organization).all()
        for organization in organizations:
            self.db.delete(organization)

        self.db.commit()
