from fastapi import APIRouter
from app.dtos.organizations import Organization
from app.services.organizations import OrgsServ


router = APIRouter(
    prefix='/api/organizations',
    tags=['Organizations']
)


@router.get("/{org_id}")
async def get_org_by_id(org_id: int, service: OrgsServ) -> Organization:
    organization = service.get_by_id(org_id)
    return organization
