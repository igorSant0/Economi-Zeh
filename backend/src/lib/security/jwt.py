from datetime import datetime, timedelta, timezone
import jwt
from src.config.envs_config import settings

SECRET_KEY: str = settings.SECRET_KEY
JWT_EXPIRATION: str = settings.JWT_EXPIRATION
ALGORITHM: str = settings.ALGORITHM


def parse_timedelta(time_str: str) -> timedelta:
    time_str = time_str.strip().lower()

    if time_str.endswith("d"):
        return timedelta(days=int(time_str[:-1]))
    elif time_str.endswith("h"):
        return timedelta(hours=int(time_str[:-1]))
    elif time_str.endswith("min"):
        return timedelta(minutes=int(time_str[:-3]))
    elif time_str.endswith("s"):
        return timedelta(seconds=int(time_str[:-1]))
    else:
        raise ValueError(f"Invalid time format: {time_str}")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + parse_timedelta(JWT_EXPIRATION)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")
