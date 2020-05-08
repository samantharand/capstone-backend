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


# lat and long for location -- check peewee docs

# tags -- a new model w a through table to attach tag to post/artwork  (Many to many -- possibly without additional model)
	# 1. through table -- maybe a separate model ** 

	# 2. let people type what ever they want, sunshine is different from sun shine
			# search and autocomplete

def init():
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True)
	print('Connected to the database!')

	DATABASE.close()