from sqlalchemy import func
from model import User, User_Cards, Cards, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print("users")

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.strip()
        user_id, email, username, password = row.split("|")

        user = User(user_id=user_id,
                    email=email,
                    username=username,
                    password=password)

        db.session.add(user)

        if i % 100 ==0:
            print(i)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database."""

    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    query = "SELECT setval(users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def load_library():

    print("library")

    for i, row in enumerate(open("seed_data/l.library")):
        row = row.strip()
        User_cards_id, card_id, user_id = row.split("|")

        library = User_Cards(User_cards_id=User_cards_id,
                            card_id=card_id,
                            user_id=user_id)

        db.session.add(library)

        if i % 100 ==0:
            print(i)

    db.session.commit()


def load_card():

    print("cardInfo")

    for i, row in enumerate(open("seed_data/c.cardInfo")):
        row = row.strip()
        card_id, name, image, text = row.split("|")

        card = Cards(card_id=card_id,
                            name=name,
                            image=image,
                            text=text)

        db.session.add(card)

        if i % 100 ==0:
            print(i)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_library()
    load_card()

    db.session.commit()