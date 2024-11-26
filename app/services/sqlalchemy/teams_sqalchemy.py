from app.custom_exceptions.notfound import NotFoundException
from app.db_mysql import DB
from app.models import Team
from app.services.base_services.teams_base_service import TeamsBaseService


class TeamsServiceSqlalchemy(TeamsBaseService):
    def __init__(self, db: DB):
        self.db = db

    def get_by_id(self, team_id) -> Team:
        team = self.db.query(Team).filter(Team.id == team_id).first()
        if team is None:
            raise NotFoundException("Team not found")
        return team