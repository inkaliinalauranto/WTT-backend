from typing import Annotated
from fastapi import Depends
from app.db import DbMySql
from app.services.base_services.organizations_base_service import OrganizationsBaseService
from app.services.sqlalchemy.organizations_sqlalchemy import OrganizationsServiceSqlAlchemy


def organizations_service_factory(context: DbMySql):
    return OrganizationsServiceSqlAlchemy(context)

OrganizationsServ = Annotated[OrganizationsBaseService, Depends(organizations_service_factory)]