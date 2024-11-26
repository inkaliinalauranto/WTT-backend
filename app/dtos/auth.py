from pydantic import BaseModel


class AuthUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    role_id: int
    team_id: int

    class Config:
        from_attributes = True


class LoginReq(BaseModel):
    username: str
    password: str


class LoginRes(BaseModel):
    access_token: str
    auth_user: AuthUser

    class Config:
        from_attributes = True


class RegisterReq(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    role_id: int
    team_id: int
