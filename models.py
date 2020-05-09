from peewee import *
import datetime

from flask_login import UserMixin

DATABASE = SqliteDatabase('streetart.sqlite', pragmas = {"foreign_keys": 1})

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()
	zip_code = CharField(max_length=5)
	bio = TextField()
	date_registered = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

class StreetArt(Model):
	name = CharField()
	location = FloatField() # indexes????? -- lat and long ?
	year = IntegerField()
	artist = CharField()
	description = TextField()
	poster = ForeignKeyField(User, backref='streetart', on_delete='CASCADE')
	date_posted = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE
# lat and long for location -- check peewee docs

# tags -- a new model w a through table to attach tag to post/artwork  (Many to many -- possibly without additional model)
	# 1. through table -- maybe a separate model ** 

	# 2. let people type what ever they want, sunshine is different from sun shine
			# search and autocomplete


# Bookmarks?? -- ones you want to visit


# class Tag(Model):
# 	name = CharField()


# class PostTag(Model):
# 	post = ForeignKeyField(StreetArt)
# 	tag = ForeignKeyField(Tag)
# 	class Meta:
# 		primary_key = CompositeKey('streetart', 'tag')

def init():
	DATABASE.connect()
	DATABASE.create_tables([User, StreetArt], safe=True)
	print('Connected to the database!')

	DATABASE.close()