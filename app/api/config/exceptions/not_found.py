from config.base_classes.base_exception import CustomBaseException
from config.http.status_codes import StatusCodes


class NotFoundException(CustomBaseException):
    def __init__(self, message: str, status_code: int = StatusCodes.NOT_FOUND):
        super().__init__(message, status_code)
