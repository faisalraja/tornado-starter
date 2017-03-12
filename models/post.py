from peewee import *
from lib.basemodel import BaseModel


class Post(BaseModel):
    title = CharField()
    content = TextField()
