from fastapi.responses import JSONResponse

from config.http.status_codes import StatusCodes


class BaseSerializer:

    @staticmethod
    def serialize(params, status_code: int = StatusCodes.OK):
        return JSONResponse(
            {"data": params, "status_code": status_code}, status_code=status_code
        )
