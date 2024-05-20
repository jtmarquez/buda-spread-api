from fastapi import APIRouter

from routes.types.base_response import GenericResponse
from routes.types.health_types import GetHealthResponseType
from serializers.base_serializer import BaseSerializer


router = APIRouter()


@router.get("/", response_model=GenericResponse[GetHealthResponseType])
def get():

    return BaseSerializer.serialize({"health_status": "ok"})
