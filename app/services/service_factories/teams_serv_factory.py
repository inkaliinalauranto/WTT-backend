from typing import Annotated
from fastapi import Depends
from app.db import DbMySql
from app.services.base_services.teams_base_service import TeamsBaseService
from app.services.sqlalchemy.teams_sqalchemy import TeamsServiceSqlalchemy


def teams_service_factory(context: DbMySql):
    return TeamsServiceSqlalchemy(context)


TeamsServ = Annotated[TeamsBaseService, Depends(teams_service_factory)]