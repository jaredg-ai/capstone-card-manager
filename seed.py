from sqlalchemy import func
from model import User, User_Cards, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print("Users")

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.strip()
        user_id, email, username, password = row.split("|")

        user = User(user_id=user_id,
                    email=email,
                    username=username)

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


if __name__ == "__name__":
    connect_to_db(app)
    db.create_all()

    load_users()