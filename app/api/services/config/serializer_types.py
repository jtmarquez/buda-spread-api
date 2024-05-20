from pydantic import BaseModel


class SerializedMarket(BaseModel):
    pair_name: str


class SerializedMarketAsk(BaseModel):
    market_id: str
    value: float
    created_at: str


class SerializedMarketBid(BaseModel):
    market_id: str
    value: float
    created_at: str


class SerializedMarketSpread(BaseModel):
    spread: float
    bid: SerializedMarketBid
    ask: SerializedMarketAsk
    calculated_at: str


class SerializedUserSpread(BaseModel):
    market_id: str
    value: float
