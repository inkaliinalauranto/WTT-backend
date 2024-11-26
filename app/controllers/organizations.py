from fastapi import APIRouter

from app import models
from app.dtos.organizations import Organization
from app.services.service_factories.organizations_serv_factory import OrganizationsServ



router = APIRouter(
    prefix='/api/organizations',
    tags=['Organizations']
)


@router.get("/{org_id}")
async def get_org_by_id(org_id: int, service: OrganizationsServ) -> Organization:
    organization: models.Organization = service.get_by_id(org_id)
    return Organization.model_validate(organization)
