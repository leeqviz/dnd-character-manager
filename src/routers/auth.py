from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs import settings
from src.db import get_psql_session
from src.schemas.auth import LoginSchema, MeSchema, TokenSchema
from src.services.auth import AuthService
from src.utils.auth import decode_jwt, issue_access_token, validate_password

http_bearer_scheme = HTTPBearer(auto_error=True)
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
) -> LoginSchema:
    unauth_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username, email or password",
    )
    user = await auth_service.get_user_credentials(name, email)
    if not user:
        raise unauth_ex
    if not validate_password(password, user.password):
        raise unauth_ex
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


@auth_router.post("/login")
async def login(user: Annotated[LoginSchema, Depends(validate_login)]) -> TokenSchema:
    claims = {
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
        # "roles": user.roles,
    }
    token = issue_access_token(str(user.id), claims)
    return TokenSchema(access_token=token, token_type=settings.jwt.token_type)


async def get_auth_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MeSchema:
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        ) from e
    user = MeSchema.model_validate(payload)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    db_user = await auth_service.get_user_credentials(user.name, user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        )

    return user


@auth_router.get("/me")
async def me(user: Annotated[MeSchema, Depends(get_auth_user)]) -> MeSchema:
    return user
