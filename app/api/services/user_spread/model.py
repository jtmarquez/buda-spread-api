from peewee import ForeignKeyField, FloatField

from config.base_classes.base_model import BaseModel
from services.market.model import Market


class UserSpread(BaseModel):
    market = ForeignKeyField(Market, field="pair_name")
    value = FloatField(null=False)

    def serialize(self):
        return {
            "id": str(self.id),
            "market_id": self.market_id,
            "value": self.value,
        }
