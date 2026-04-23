from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_psql_session
from src.schemas.auth import LoginSchema, TokenSchema
from src.services.auth import AuthService
from src.utils.auth import create_access_token, validate_password

auth_router = APIRouter()


def get_auth_service(
    session: AsyncSession = Depends(get_psql_session),
) -> AuthService:
    return AuthService(session)


async def validate_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    unauth_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username, email or password",
    )
    user = await auth_service.get_by_name_and_email(name, email)
    if not user:
        raise unauth_ex
    if not validate_password(password, user.password):
        raise unauth_ex
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return LoginSchema.model_validate(user)


@auth_router.post("/login")
async def login(user: Annotated[LoginSchema, Depends(validate_login)]) -> TokenSchema:
    payload = {
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
    }
    token = create_access_token(payload)
    return TokenSchema(access_token=token, token_type="Bearer")
