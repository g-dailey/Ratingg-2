"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
@app.route("/homepage.html")
def home():
    return render_template("homepage.html")

@app.route("/movies")
def all_movie():
    movies = crud.get_movies()
    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/users", methods=['POST'])
def check_user():
    email = request.form.get('email')
    password = request.form.get('password')
    if crud.get_user_by_email(email):
        flash('Sorry you cannot create an account with this email because it already exist')
    else:
         user = crud.create_user(email, password)
         db.session.add(user)
         db.session.commit()
         flash("Account created! Please Log in.")
    return redirect("/")



@app.route("/login", methods=["POST"])
def login_user():
    """Login the user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user:
        flash("You do not have a registered account, please register first!", "danger")
    else:
        session["email"] = email
        flash("Loged in Successfully")

    return redirect("/")

@app.route("/love-movie/<movie_id>", methods=["POST"])
def love_movie(movie_id):

    if "email" in session:
        user = crud.get_user_by_email(session["email"])
        movie = crud.get_movie_by_id(movie_id)
        rating = request.form.get("loved_movie_key")
        create_rating = crud.create_rating(user, movie, rating)

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
