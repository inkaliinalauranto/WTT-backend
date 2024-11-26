from typing import Annotated
import dotenv
from fastapi import Depends
from app.db import DbMySql
from app.services.base_services.auth_base_service import AuthBaseService
from app.services.sqlalchemy.auth_sqlalchemy import AuthServiceSqlAlchemy


# Luodaan authservicelle factory skaalautuvuuden varalle.
def auth_service_factory(context: DbMySql):
    return AuthServiceSqlAlchemy(context)


# Palautetaan AuthBaseService.
# sqlalchemyllä tehty AuthServiceSqlAlchemy service AuthBaseServicen child
AuthServ = Annotated[AuthBaseService, Depends(auth_service_factory)]