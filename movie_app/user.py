"""Table User"""

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String(255), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)
    film = db.relationship("Film", backref='user', lazy=True)

    def __init__(self, login, password):
        self.login = login
        self.password = password
