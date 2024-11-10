from pydantic import BaseModel


class AuthUser(BaseModel):
    id: int
    username: str
    role_id: int
    team_id: int


class LoginReq(BaseModel):
    username: str
    password: str


class LoginRes(BaseModel):
    access_token: str
    auth_user: AuthUser
