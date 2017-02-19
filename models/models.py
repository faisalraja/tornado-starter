from peewee import *
from lib.basemodel import BaseModel


class User(BaseModel):
    email = CharField()
    name = CharField()
    password = CharField(null=True)

    auth_key = CharField(null=True)

    @classmethod
    def get_user_by_oauth(cls, result):
        auth_key = '{}-{}'.format(result.provider.__class__.__name__, result.user.id)

        try:
            user = cls(cls.auth_key == auth_key).get()
        except DoesNotExist:
            user = cls(email=result.user.email, name=result.user.name)
            user.save()

        return user


class Post(BaseModel):
    title = CharField()
    content = TextField()
