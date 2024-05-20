from config.http.status_codes import StatusCodes


class CustomBaseException(Exception):
    def __init__(self, message: str, status_code: int = StatusCodes.INTERNAL_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
