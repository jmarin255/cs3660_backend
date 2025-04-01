from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    sucess: bool
    jwt_token: str|None=None


class VerifyLginRequest(BaseModel):
    jwt_token: str
    