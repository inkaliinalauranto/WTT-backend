from typing import Annotated
from fastapi import Depends
from app.db import DbMySql
from app.services.base_services.roles_base_service import RolesBaseService
from app.services.sqlalchemy.roles_sqlalchemy import RolesServiceSqlalchemy


def roles_service_factory(context: DbMySql):
    return RolesServiceSqlalchemy(context)


RolesServ = Annotated[RolesBaseService, Depends(roles_service_factory)]