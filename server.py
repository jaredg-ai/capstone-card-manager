from typing_extensions import Required
from flask import Flask, render_template, request, flash, redirect, session

app = Flask(__name__)


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
    user = request.form["user"]
    password = request.form["password"]

    new_user = User(email=email, user=user, password=password)

    flash(f"User {email} added.")
    return redirect(f"/users/{new_user.user_id}")


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
    return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Logged out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")