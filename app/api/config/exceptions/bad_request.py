from config.base_classes.base_exception import CustomBaseException
from config.http.status_codes import StatusCodes


class BadRequestException(CustomBaseException):
    def __init__(self, message: str, status_code: int = StatusCodes.BAD_REQUEST):
        super().__init__(message, status_code)
