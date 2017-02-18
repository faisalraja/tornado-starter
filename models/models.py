from peewee import *
import config
from playhouse.db_url import connect


db = connect(**config.db)


class BaseModel(Model):

    class Meta:
        database = db


class Post(BaseModel):
    title = CharField()
    content = TextField()


db.connect()
db.create_tables([Post], safe=True)
db.close()