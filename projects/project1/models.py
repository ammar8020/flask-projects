import flask
from project1 import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):

    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class Movie(db.Document):
    movie_id = db.StringField(max_length=10, unique=True)
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    year = db.IntField()
    category = db.StringField(max_length=25)


class Watchlist(db.Document):
    user_id = db.IntField()
    movie_id = db.StringField(max_length=10)
