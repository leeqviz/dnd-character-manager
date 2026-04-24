from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    password: bytes
    is_active: bool = True
    # TODO add roles
    # roles: list[str]

    model_config = ConfigDict(from_attributes=True)


class MeSchema(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True
    sub: str
    iss: str
    iat: int
    exp: int
    nbf: int

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
