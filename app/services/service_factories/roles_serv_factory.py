import os
from typing import Annotated
import dotenv
from fastapi import Depends

from app.db_mysql import DB
from app.services.base_services.roles_base_service import RolesBaseService
from app.services.sqlalchemy.roles_sqlalchemy import RolesServiceSqlalchemy


dotenv.load_dotenv()

def roles_service_factory(context: DB):
    if os.getenv("DB") == "mysql":
        return RolesServiceSqlalchemy(context)

    raise Exception("RolesService is not initialized. Check if DB attribute is correct in .env")

RolesServ = Annotated[RolesBaseService, Depends(roles_service_factory)]