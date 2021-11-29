"""Table User"""
from flask_login import UserMixin
from filmapp import db



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String(255), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)
    admin = db.Column(db.Boolean)
    film = db.relationship("Film", backref='user', lazy=True)

    def __init__(self, login, password, admin):
        self.login = login
        self.password = password
        self.admin = admin





