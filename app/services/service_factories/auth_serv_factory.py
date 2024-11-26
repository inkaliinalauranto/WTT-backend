from typing import Annotated
import dotenv
from fastapi import Depends
from app.db_mysql import DB
from app.services.base_services.auth_base_service import AuthBaseService
from app.services.sqlalchemy.auth_sqlalchemy import AuthServiceSqlAlchemy
import os


dotenv.load_dotenv()

# Luodaan authservicelle factory skaalautuvuuden varalle.
def auth_service_factory(context: DB):
    if os.getenv("DB") == "mysql":
        return AuthServiceSqlAlchemy(context)

    # Jos serviceä ei onnistuta initialisoimaan .envissä olevan väärän nimen takia, palautetaan virhe devaajalle
    raise Exception("AuthService is not initialized. Check if DB attribute is correct in .env")


# Palautetaan AuthBaseService.
# sqlalchemyllä tehty AuthServiceSqlAlchemy service AuthBaseServicen child
AuthServ = Annotated[AuthBaseService, Depends(auth_service_factory)]