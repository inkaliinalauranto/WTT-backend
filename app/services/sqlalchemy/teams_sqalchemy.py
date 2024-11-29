from app.custom_exceptions.notfound import NotFoundException
from app.custom_exceptions.taken import TakenException
from app.models import Team
from app.services.base_services.teams_base_service import TeamsBaseService


class TeamsServiceSqlalchemy(TeamsBaseService):
    def get_by_id(self, team_id) -> Team:
        team = self.db.query(Team).filter(Team.id == team_id).first()
        if team is None:
            raise NotFoundException("Team not found")
        return team


    def create_team_if_not_exist(self, team_name: str, org_id: int) -> Team:
        try:
            team = self.db.query(Team).filter(Team.name == team_name).first()
            if team is None:
                new_team = Team(name=team_name, organization_id=org_id)
                self.db.add(new_team)
                self.db.commit()
                self.db.refresh(new_team)
                return new_team

            raise TakenException("Team already exists")

        except Exception as e:
            self.db.rollback()
            raise e