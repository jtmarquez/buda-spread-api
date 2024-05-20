from peewee import ForeignKeyField, FloatField

from utils.date_to_string import string_to_date
from config.base_classes.base_model import BaseModel
from services.market.model import Market


class MarketAsk(BaseModel):
    market = ForeignKeyField(Market, field="pair_name", backref="asks")
    value = FloatField(null=False)

    def serialize(self):
        return {
            "market_id": self.market.pair_name,
            "value": self.value,
            "created_at": string_to_date(self.created_at),
        }
