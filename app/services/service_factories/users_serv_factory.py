from typing import Annotated
from fastapi import Depends
from app.db import DbMySql
from app.services.base_services.users_base_service import UsersBaseService
from app.services.sqlalchemy.users_sqlalchemy import UsersServiceSqlAlchemy



def users_service_factory(context: DbMySql):
    return UsersServiceSqlAlchemy(context)


# Tämän toimintaperiaate on sama kuin databasen luonnissa.
# Alla olevassa annotated funktiossa injektoidaan tietokantayhteys UsersBaseServicelle.
# UsersBaseService injektoidaan nyt välittämällä tämä muuttuja parametrinä controllerin functioon -> (service: UsersServ).
UsersServ = Annotated[UsersBaseService, Depends(users_service_factory)]