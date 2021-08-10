from operator import index, truediv
from flask_sqlalchemy import SQLAlchemy
import correlation
from collections import defaultdict


db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), nullable=True)
    username = db.Column(db.string(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)

    def __repr__(self):

        return f"<User user_id={self.user_id} email={self.email}"


class User_Cards(db.Model):

    __tablename__ = "library"

    User_cards_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.card_id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), index=True)