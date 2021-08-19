from os import name
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import connect_to_db, db, User, User_Cards, Cards
import magic

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
    username = request.form.get("username")
    password = request.form["password"]

    new_user = User(email=email, username=username, password=password)
    
    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.user_id
    flash(f"User {username} added.")
    return redirect(f"/library")
    

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("incorrect password")
        return  redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/library")


@app.route('/logout')
def logout():
    """Logged out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/library')
def user_cards_list():
    """Show list of users cards."""

    user_cards = User_Cards.query.filter_by(user_id=session["user_id"])
    return render_template("library.html", user_cards=user_cards)


@app.route("/magicCards/search")
def search_magic_cards():
    """Lets user search for magic cards."""

    #get card name from request.
    #That name would bring up the appropriate card from the api.
    #show template of the cards.
    name = request.args["name"]
    results = magic.search_by_name(name)

    return render_template("/searchResults.html", results=results, name=name)
    

@app.route("/library/addedCards/<cardid>", methods=["POST"])
def add_cards_library(cardid):
    """When the user finds the card they wanted to add, this adds the card to the library."""

    #when the user finds the card they want, add that card to their library.
    #return to their library with the card shown
    cardinfo = magic.search_by_id(cardid)

    card = Cards(name=cardinfo.name, image=cardinfo.image_url, text=cardinfo.text)
    db.session.add(card)
    db.session.commit()
    user_card = User_Cards(card_id=card.card_id, user_id=session["user_id"])
    db.session.add(user_card)
    db.session.commit()
    return redirect("/library")



if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")