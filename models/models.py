from peewee import *
import config
from playhouse.db_url import connect


db = connect(config.db_connection,
             max_connections=20,
             stale_timeout=600)


class BaseModel(Model):

    class Meta:
        database = db


class Post(BaseModel):
    title = CharField()
    content = TextField()


print('Called Models')
db.connect()
db.create_tables([Post], safe=True)
db.close()