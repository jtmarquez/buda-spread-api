from config.base_classes.base_model import BaseModel
from peewee import CharField


class Market(BaseModel):
    pair_name = CharField(unique=True, null=False, index=True)

    def serialize(self):
        return {
            "pair_name": self.pair_name,
        }
