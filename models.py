
import config_db
from peewee import *
from datetime import datetime

DBASE = MySQLDatabase(
    database=config_db.db_n,
    user = config_db.db_u,
    password = config_db.db_p,
    host='localhost'
)


class BaseModel(Model):
    class Meta:
        database = DBASE


class ChatUser(BaseModel):
    id = BigIntegerField(unique=True)
    #chat_id = BigIntegerField(unique=True))
    said_name = CharField(max_length = 225, null =True)
    first_name = CharField(max_length = 225, null =True)
    last_name = CharField(max_length = 225, null =True)
    username = CharField(max_length = 225, null =True)
    phone = CharField(max_length = 225, null =True)
    birth = CharField(max_length = 100, null =True)
    subscribed = IntegerField()

    created_at = DateTimeField(default=datetime.now)
    class Meta:
        database = DBASE
        table_name = 'chat_user'


class Loghook(BaseModel):
    id = AutoField()
    chat_id = BigIntegerField()
    fulljson = TextField()
    created_at = DateTimeField(default=datetime.now)
    class Meta:
        database = DBASE
        table_name = 'log_hook'


class TimerTask(BaseModel):
    """"""
    id = AutoField() #уникальный id
    chat_id = BigIntegerField()
    start = DateTimeField(500)
    message_id = IntegerField()
    status = IntegerField()
    url = CharField(300)
    lenght = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DBASE
        table_name = 'timer_task'


class PlaylistUser(BaseModel):
    """"""
    id = AutoField() #уникальный id
    chat_id = BigIntegerField()
    playlist_id = BigIntegerField()
    status = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DBASE
        table_name = 'playlist_user'


class Playlist(BaseModel):
    """"""
    id = AutoField() #уникальный id
    chat_id = BigIntegerField()
    start_at = DateTimeField(500)
    url = CharField(500)
    status = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DBASE
        table_name = 'playlist'


class ChatFunnel(BaseModel):
    id = AutoField()
    chatuser_id = IntegerField()
    type = IntegerField()
    chatfunnel = CharField(50)
    message = TextField()
    created_at = DateTimeField(default=datetime.now)
    class Meta:
        database = DBASE
        table_name = 'chat_funnel'


class ChatFeedback(BaseModel):

    id = AutoField()
    chatuser_id = IntegerField()
    name = CharField(250)
    phone = CharField(250)
    location = CharField(250)
    message = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DBASE
        table_name = 'chat_feedback'
