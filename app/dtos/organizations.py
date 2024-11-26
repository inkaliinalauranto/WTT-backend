from pydantic import BaseModel


class Organization(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True