import os
from typing import Annotated
import dotenv
from fastapi import Depends
from app.db_mysql import DB
from app.services.base_services.organizations_base_service import OrganizationsBaseService
from app.services.sqlalchemy.organizations_sqlalchemy import OrganizationsServiceSqlAlchemy

dotenv.load_dotenv()

def organizations_service_factory(context: DB):
    if os.getenv("DB") == "mysql":
        return OrganizationsServiceSqlAlchemy(context)

    raise Exception("OrganizationsService is not initialized. Check if DB attribute is correct in .env")

OrganizationsServ = Annotated[OrganizationsBaseService, Depends(organizations_service_factory)]