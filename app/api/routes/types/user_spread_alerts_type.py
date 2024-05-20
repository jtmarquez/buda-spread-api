from pydantic import BaseModel
from services.config.serializer_types import (
    SerializedMarketSpread,
    SerializedUserSpread,
)


class GetUserSpreadAlertsType(BaseModel):
    saved_spread: SerializedUserSpread
    current_spread: SerializedMarketSpread | None


CreateUserSpreadAlertType = SerializedUserSpread
