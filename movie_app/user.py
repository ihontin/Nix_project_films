"""Table User"""
from flask_login import UserMixin
from app import db, api
from flask_restx import fields

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

model_user = api.model(
    "Film", {
        "id": fields.Integer(required=True),
        "login": fields.String(required=True),
        "password": fields.String(required=True),
        "admin": fields.String(required=True)})

