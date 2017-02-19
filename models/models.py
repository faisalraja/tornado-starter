from peewee import *
import config
from lib.basemodel import BaseModel
from passlib.hash import bcrypt_sha256


class User(BaseModel):
    # Can be email or oauth id
    auth_id = CharField()
    name = CharField()

    email = CharField(null=True)
    password = CharField(null=True)

    @classmethod
    def get_user_by_oauth(cls, result):
        auth_id = '{}-{}'.format(result.provider.__class__.__name__, result.user.id)

        try:
            user = cls(cls.auth_id == auth_id).get()
        except DoesNotExist:
            user = cls(auth_id=auth_id,
                       email=result.user.email,
                       name=result.user.name)
            user.save()

        return user

    @classmethod
    def register(cls, **kwargs):
        auth_id = kwargs['email'].lower()

        try:
            user = cls(cls.auth_id == auth_id).get()
        except DoesNotExist:
            user = cls(auth_id=auth_id,
                       email=auth_id,
                       name=kwargs['name'],
                       password=cls.get_password(kwargs['password']))
            user.save()

        return user

    @classmethod
    def get_password(cls, password):

        return bcrypt_sha256.using(rounds=config.password_iterations).hash(password)



class Post(BaseModel):
    title = CharField()
    content = TextField()
