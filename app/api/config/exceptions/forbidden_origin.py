from config.base_classes.base_exception import CustomBaseException
from config.http.status_codes import StatusCodes


class ForbiddenOriginException(CustomBaseException):
    def __init__(self, message: str, status_code: int = StatusCodes.FORBIDDEN):
        super().__init__(message, status_code)
