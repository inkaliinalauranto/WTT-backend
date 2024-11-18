from typing import Annotated
from fastapi import Depends
from app.db import DB
from app.models import Role


class RolesService:
    def __init__(self, db):
        self.db = db

    # Haetaan käyttäjä id:n perusteella:
    def get_by_id(self, role_id) -> Role:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        return role


def get_service(db: DB):
    return RolesService(db)


RolesServ = Annotated[RolesService, Depends(get_service)]
