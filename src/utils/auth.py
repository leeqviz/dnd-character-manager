from datetime import timedelta

import bcrypt
import jwt

from src.configs import settings
from src.utils import timestamp_with_tz


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
):
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def issue_access_token(
    subject: str,
    extra_claims: dict | None = None,
    expires_in: int = settings.jwt.access_token_expire_minutes,
    expires_delta: timedelta | None = None,
):
    now = timestamp_with_tz
    expire = now + (expires_delta or timedelta(minutes=expires_in))

    payload = {
        "sub": subject,
        "iss": settings.app.name,
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
    }

    if extra_claims:
        payload.update(extra_claims)

    return encode_jwt(payload)


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
