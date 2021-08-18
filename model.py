from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict


db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)

    def __repr__(self):

        return f"<User user_id={self.user_id} email={self.email}"


class User_Cards(db.Model):

    __tablename__ = "library"

    User_cards_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.card_id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), index=True)


def connect_to_db(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cards'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__name__":

    from server import app

    connect_to_db(app)
    print("Connected to DB")