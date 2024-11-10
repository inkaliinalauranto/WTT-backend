from pydantic import BaseModel


# Tänne tulee kaikki datamallit, jotka löytyvät sellaisenaan tietokannasta
# Näitä malleja kannattaa käyttää kun tekee tietokantaan inserttejä tai updatea.


class Test(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    access_jti: str
    role_id: int
    team_id: int

    class Config:
        orm_mode = True


class Role(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Team(BaseModel):
    id: int
    name: str
    organization_id: int

    class Config:
        orm_mode = True


class Organization(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
