from project1 import app
from flask import render_template


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", login=False)


@app.route("/login")
def login():
    return render_template("login.html", login=False)


@app.route("/movies")
def movies():
    return render_template("movies.html", login=False)


@app.route("/register")
def register():
    return render_template("register.html", login=False)
