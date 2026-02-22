from dataclasses import dataclass

@dataclass(frozen=True)
class _UserPaths:
    PREFIX: str = "/user"
    GET_BY_ID: str = "/{user_id}"
    CONFIRM_EMAIL: str = "/confirm-email"

@dataclass(frozen=True)
class _AuthPaths:
    PREFIX: str = "/auth"
    LOGIN: str = "/login"
    REFRESH: str = "/refresh"

class PathConfig:

    user = _UserPaths()
    auth = _AuthPaths()

paths = PathConfig()