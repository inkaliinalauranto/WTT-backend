
from typing import Annotated
import dotenv
from fastapi import Depends

from app.db_mysql import DB
import os

from app.services.base_services.users_base_service import UsersBaseService
from app.services.sqlalchemy.users_sqlalchemy import UsersServiceSqlAlchemy


dotenv.load_dotenv()

def users_service_factory(context: DB):
    if os.getenv("DB") == "mysql":
        return UsersServiceSqlAlchemy(context)
    
    raise Exception("UsersService is not initialized. Check if DB attribute is correct in .env")

# Tämän toimintaperiaate on sama kuin databasen luonnissa.
# Alla olevassa annotated funktiossa injektoidaan tietokantayhteys UsersBaseServicelle.
# UsersBaseService injektoidaan nyt välittämällä tämä muuttuja parametrinä controllerin functioon -> (service: UsersServ).
UsersServ = Annotated[UsersBaseService, Depends(users_service_factory)]