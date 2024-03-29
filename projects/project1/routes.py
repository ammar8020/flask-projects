from project1 import app, db
from flask import (
    render_template,
    request,
    json,
    Response,
    redirect,
    flash,
    url_for,
    session,
)
from project1.models import User, Movie, Watchlist
from project1.forms import LoginForm, RegisterForm


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if session.get("username"):
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(
            user_id=user_id, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.save()
        flash("User registered successfully", "success")
        return redirect(url_for("index"))

    return render_template("register.html", title="Register", form=form)


@app.route("/watchlist", methods=["GET", "POST"])
def watchlist():

    if not session.get("username"):
        return redirect(url_for("login"))

    movie_id = request.form.get("movie_id")
    movie_title = request.form.get("title")
    user_id = session.get("user_id")

    if movie_id:
        if Watchlist.objects(user_id=user_id, movie_id=movie_id):
            flash(f"You have already added  {movie_title} to your Watchlist", "danger")
            return redirect(url_for("movies"))
        else:
            Watchlist(user_id=user_id, movie_id=movie_id).save()
            flash(f"{movie_title} has been added to your watchlist", "success")

    classes = list(
        User.objects.aggregate(
            *[
                {
                    "$lookup": {
                        "from": "watchlist",
                        "localField": "user_id",
                        "foreignField": "user_id",
                        "as": "r1",
                    }
                },
                {
                    "$unwind": {
                        "path": "$r1",
                        "includeArrayIndex": "r1_id",
                        "preserveNullAndEmptyArrays": False,
                    }
                },
                {
                    "$lookup": {
                        "from": "movie",
                        "localField": "r1.movie_id",
                        "foreignField": "movie_id",
                        "as": "r2",
                    }
                },
                {"$unwind": {"path": "$r2", "preserveNullAndEmptyArrays": False}},
                {"$match": {"user_id": user_id}},
                {"$sort": {"movie_id": 1}},
            ]
        )
    )

    return render_template("watchlist.html", title="Watchlist", classes=classes)


@app.route("/users")
def users():
    users = User.objects.all()
    return render_template("users.html", users=users)


@app.route("/logout")
def logout():
    session["user_id"] = False
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/trending")
def trending():
    return render_template("trending.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()

        if user and user.get_password(password):
            flash(f"{user.first_name}, has successfully logged in!", "success")
            session["user_id"] = user.user_id
            session["username"] = user.first_name
            return redirect("/")
        else:
            flash("Login Credentials not correct", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/movies/")
@app.route("/movies/<year>")
def movies(year="2019"):
    classes = Movie.objects.order_by("+movie_id")
    return render_template("movies.html", movies_data=classes, year=year)
