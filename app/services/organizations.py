from typing import Annotated
from fastapi import Depends
from app.db import DB
from app.models import Organization


class OrganizationsService:
    def __init__(self, db:DB):
        self.db = db

    def get_by_id(self, org_id) -> Organization:
        organization = self.db.query(Organization).filter(Organization.id == org_id).first()
        return organization


def get_service(db: DB):
    return OrganizationsService(db)


OrgsServ = Annotated[OrganizationsService, Depends(get_service)]
