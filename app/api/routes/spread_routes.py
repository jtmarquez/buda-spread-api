from fastapi import APIRouter, Path

from routes.types.base_response import GenericResponse
from routes.types.spread_types import GetSpreadResponseType
from controllers.spread import SpreadController
from serializers.spread_serializer import SpreadSerializer


router = APIRouter()


@router.get(
    "/",
    response_model=GenericResponse[GetSpreadResponseType],
    description="Endpoint for obtaining the spreads for all markets",
)
def get_all_spreads():
    spreads_response = SpreadController.get_spreads()

    return SpreadSerializer.serialize(spreads_response)


@router.get(
    "/{market_id}",
    response_model=GenericResponse[GetSpreadResponseType],
    description="Endpoint for obtaining the spread for a specific market",
)
def get_spread(market_id: str = Path(example="BTC-CLP")):
    spreads_response = SpreadController.get_spreads(market_id)

    return SpreadSerializer.serialize(spreads_response)
