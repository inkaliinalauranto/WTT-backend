from typing import Annotated
from fastapi import Depends
from app.db import DB
from app.models import Team


class TeamsService:
    def __init__(self, db:DB):
        self.db = db

    def get_by_id(self, team_id) -> Team:
        team = self.db.query(Team).filter(Team.id == team_id).first()
        return team


def get_service(db: DB):
    return TeamsService(db)


TeamsServ = Annotated[TeamsService, Depends(get_service)]
