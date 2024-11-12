from pydantic import BaseModel


class Test(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
