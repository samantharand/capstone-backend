from peewee import *
import datetime

from flask_login import UserMixin

DATABASE = SqliteDatabase('streetart.sqlite')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()
	zip_code = CharField(max_length=5)
	bio = TextField()
	date_registered = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE


def init():
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True)
	print('Connected to the database!')

	DATABASE.close()