from enum import Enum


class ApiErrorStatus(Enum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    CONFLICT = 409
    PAYMENT_REQUIRED = 402
    PAYLOAD_TOO_LARGE = 413


class ApiError(Exception):
    status_code: int
    message: str
    stack: str | None

    def __init__(self, status, message, stack=None):
        super().__init__(message)
        self.message = message
        self.stack = stack

        if isinstance(status, int):
            self.status_code = status
        elif isinstance(status, str):
            self.status_code = ApiErrorStatus[status].value
        elif isinstance(status, ApiErrorStatus):
            self.status_code = status.value
        else:
            self.status_code = ApiErrorStatus.INTERNAL_SERVER_ERROR.value
