from fastapi import APIRouter, Path, Body

from config.http.status_codes import StatusCodes
from routes.types.base_response import GenericResponse
from routes.types.user_spread_alerts_type import (
    CreateUserSpreadAlertType,
    GetUserSpreadAlertsType,
)
from controllers.user_spread_alerts import UserSpreadAlertController
from serializers.user_spread_alert_serializer import UserSpreadAlertSerializer


router = APIRouter()


@router.get(
    "/{spread_id}",
    response_model=GenericResponse[GetUserSpreadAlertsType],
    description="Endpoint for obtaining the spread information for a created user spread",
)
def get_user_spread_alerts(spread_id: str = Path(example="550e8400-e29b-41d4-a716-446655440000")):
    user_spread_alert = UserSpreadAlertController.get_user_spread_alerts(spread_id)

    return UserSpreadAlertSerializer.serialize(user_spread_alert)


@router.post(
    "/",
    response_model=GenericResponse[CreateUserSpreadAlertType],
    description="Endpoint for creating a user spread",
    status_code=StatusCodes.CREATED,
)
def create_user_spread_alert(
    market_id: str = Body(example="BTC-CLP"), spread: float = Body(example=128999.0)
):
    user_spread_alert = UserSpreadAlertController.create_user_spread_alert(
        market_id=market_id, spread=spread
    )

    return UserSpreadAlertSerializer.serialize(
        params=user_spread_alert, status_code=StatusCodes.CREATED
    )
