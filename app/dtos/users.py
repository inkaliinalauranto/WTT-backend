from pydantic import BaseModel


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
