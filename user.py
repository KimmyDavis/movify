from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, password):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.password = password


    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE sn = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[2], email=user[3], profile_pic=user[4], password=user[5]
        )
        return user

    @staticmethod
    def get_name(user_name):
        db = get_db()
        user_name = user_name.lower()
        user = db.execute(
            "SELECT *, LOWER(name) AS lower_name FROM user WHERE lower_name = ?", (user_name,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[2], email=user[3], profile_pic=user[4], password=user[5]
        )
        print(user)
        return user

    @staticmethod
    def create(id_, name, email, profile_pic, password):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic, password_hash) "
            "VALUES (?, ?, ?, ?, ?)",
            (id_, name, email, profile_pic, password),
        )
        db.commit()