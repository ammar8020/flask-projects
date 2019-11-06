from project1 import app, db
from flask import render_template, request, json, Response
from project1.models import User, Movie, Watchlist

movies_data = [
    {
        "movieID": "1111",
        "title": "PHP 111",
        "description": "Intro to PHP",
        "credits": "3",
        "term": "Fall, Spring",
    },
    {
        "movieID": "2222",
        "title": "Java 1",
        "description": "Intro to Java Programming",
        "credits": "4",
        "term": "Spring",
    },
    {
        "movieID": "3333",
        "title": "Adv PHP 201",
        "description": "Advanced PHP Programming",
        "credits": "3",
        "term": "Fall",
    },
    {
        "movieID": "4444",
        "title": "Angular 1",
        "description": "Intro to Angular",
        "credits": "3",
        "term": "Fall, Spring",
    },
    {
        "movieID": "5555",
        "title": "Java 2",
        "description": "Advanced Java Programming",
        "credits": "4",
        "term": "Fall",
    },
]


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login")
def login():
    return render_template("login.html", login=True)


@app.route("/movies/")
@app.route("/movies/<term>")
def movies(term="Spring 2019"):
    return render_template(
        "movies.html", movies_data=movies_data, movies=True, term=term
    )


@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/watchlist", methods=["GET", "POST"])
def watchlist():
    id = request.form.get("movieID")
    title = request.form.get("title")
    term = request.form.get("term")
    return render_template(
        "watchlist.html", watchlist=True, movie={"id": id, "title": title, "term": term}
    )


@app.route("/api/")
@app.route("/api/<id>")
def api(id=None):
    if id == None:
        json_data = movies_data
    else:
        json_data = movies_data[int(id)]

    return Response(json.dumps(json_data), mimetype="application/json")


@app.route("/user")
def user():
    # User(user_id=1, first_name="Ammar", last_name="Ahmed", email="ammar@gmail.com", password="1234").save()
    # User(user_id=2, first_name="Jose", last_name="Sal", email="jose@gmail.com", password="1234").save()
    users = User.objects.all()
    return render_template("user.html", users=users)
