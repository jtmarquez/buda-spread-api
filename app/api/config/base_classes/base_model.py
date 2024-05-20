import datetime
import uuid
from config.database import database
from peewee import Model, UUIDField, DateTimeField


db = database


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    deleted_at = DateTimeField(default=None, null=True)

    class Meta:
        database = db
