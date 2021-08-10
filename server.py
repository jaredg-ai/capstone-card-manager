from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from model import User, User_Cards


app = Flask(__name__)


app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    new_user = User(email=email, username=username, password=password)

    flash(f"User {email} added.")
    return redirect(f"/library/{new_user.user_id}")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.quer.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("incorrect password")
        return  redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/library/{user.user_id}")


@app.route('/logout')
def logout():
    """Logged out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/library')
def user_cards_list():
    """Show list of users cards."""

    user_cards = User_Cards.query.all()
    return render_template("library.html", user_cards=user_cards)


if __name__ == "__main__":

    app.debug = True

    app.run(host="0.0.0.0")