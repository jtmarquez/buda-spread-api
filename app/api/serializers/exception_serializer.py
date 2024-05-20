from fastapi.responses import JSONResponse
from config.http.status_codes import StatusCodes
from serializers.base_serializer import BaseSerializer


class ExceptionSerializer(BaseSerializer):

    @staticmethod
    def serialize(error: str, status_code: int = StatusCodes.INTERNAL_ERROR):
        return JSONResponse(
            {"error": error, "status_code": status_code}, status_code=status_code
        )
