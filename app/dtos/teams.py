from pydantic import BaseModel


class Team(BaseModel):
    id: int
    name: str
    organization_id: int

    class Config:
        from_attributes = True