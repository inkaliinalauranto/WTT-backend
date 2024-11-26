from typing import Annotated
from fastapi.params import Depends
from app.db import DbMySql
from app.services.base_services.shifts_base_service import ShiftsBaseService
from app.services.sqlalchemy.shifts_sqlalchemy import ShiftsServiceSqlAlchemy


def shifts_serv_factory(context: DbMySql):
    return ShiftsServiceSqlAlchemy(context)


ShiftsServ = Annotated[ShiftsBaseService, Depends(shifts_serv_factory)]
