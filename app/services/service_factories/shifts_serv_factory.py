import os
from typing import Annotated
import dotenv
from fastapi.params import Depends

from app.db_mysql import DB
from app.services.base_services.shifts_base_service import ShiftsBaseService
from app.services.sqlalchemy.shifts_sqlalchemy import ShiftsServiceSqlAlchemy

dotenv.load_dotenv()


def shifts_serv_factory(context: DB):
    if os.getenv("DB") == "mysql":
        return ShiftsServiceSqlAlchemy(context)

    raise Exception("ShiftsService is not initialized. Check if DB attribute is correct in .env")


ShiftsServ = Annotated[ShiftsBaseService, Depends(shifts_serv_factory)]
