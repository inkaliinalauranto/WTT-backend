from pydantic import BaseModel

class TestSchema(BaseModel):
    id: int
    name: str


    class Config:
        orm_mode = True