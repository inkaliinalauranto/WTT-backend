import os
from typing import Annotated
import dotenv
from fastapi import Depends

from app.db_mysql import DB
from app.services.base_services.teams_base_service import TeamsBaseService
from app.services.sqlalchemy.teams_sqalchemy import TeamsServiceSqlalchemy


dotenv.load_dotenv()

def teams_service_factory(context: DB):
    if os.getenv("DB") == "mysql":
        return TeamsServiceSqlalchemy(context)

    raise Exception("TeamsService is not initialized. Check if DB attribute is correct in .env")

TeamsServ = Annotated[TeamsBaseService, Depends(teams_service_factory)]