from config.base_classes.base_exception import CustomBaseException
from config.http.status_codes import StatusCodes


class DatabaseErrorException(CustomBaseException):
    def __init__(self, message: str, status_code: int = StatusCodes.INTERNAL_ERROR):
        super().__init__(message, status_code)
