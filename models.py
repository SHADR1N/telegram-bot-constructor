from peewee import *
from config import *

MENU = MENU.split('\\')[:-1]
MENU = '\\'.join(MENU)
db = SqliteDatabase(MENU+'\\user.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):

    user_id = IntegerField(unique=True)


    @classmethod
    def user_exists(cls, user_id):
        query = cls().select().where(cls.user_id == user_id)
        return query.exists()

    @classmethod
    def create_user(cls, user_id):
        user_id, created = cls.get_or_create(user_id=user_id)

    @classmethod
    def get_user_id_print(cls, user_id):
        return cls.get(user_id=user_id).user_id