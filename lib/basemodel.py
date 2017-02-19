import config
from peewee import *


class BaseModel(Model):

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.get(cls.id == id)
        except DoesNotExist:
            return None

    class Meta:
        database = config.db