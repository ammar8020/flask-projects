import flask
from project1 import db


class User(db.Document):

    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)


class Movie(db.Document):
    movie_id = db.StringField(max_length=10, unique=True)
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    credits = db.IntField()
    term = db.StringField(max_length=25)


class Watchlist(db.Document):
    user_id = db.IntField()
    movie_id = db.StringField(max_length=10)
