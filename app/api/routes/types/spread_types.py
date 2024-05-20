from pydantic import BaseModel

from services.config.serializer_types import SerializedMarketSpread


GetSpreadResponseType = list[SerializedMarketSpread]
