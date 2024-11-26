from fastapi import APIRouter
from app.dtos.teams import Team
from app.services.service_factories.teams_serv_factory import TeamsServ



router = APIRouter(
    prefix='/api/teams',
    tags=['Teams']
)


@router.get("/{team_id}")
async def get_team_by_id(team_id: int, service: TeamsServ) -> Team:
    team = service.get_by_id(team_id)
    return team
