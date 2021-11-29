from filmapp import api
from flask_restx import fields

model_user = api.model(
    'Film', {
        'id': fields.Integer(),
        'login': fields.String(),
        'password': fields.String(),
        'admin': fields.Boolean()})

model_login = api.model(
    'User_login', {
        'id': fields.Integer(),
        'login': fields.Boolean()})

model_register = api.model(
    'User_register', {
        'register': fields.Boolean()})

model_add = api.model(
    'Film', {
        'id': fields.Integer(),
        'added': fields.Boolean()})

model_del_director = api.model(
    'Film', {
        'id': fields.Integer(),
        'deleted': fields.Boolean()})

model_film = api.model(
    "Film", {
        "id": fields.Integer(required=True),
        "title": fields.String(required=True),
        "release": fields.Date(required=True),
        "poster": fields.String(required=True),
        "rating": fields.Integer(required=True),
        "description": fields.String(required=False),
        "fk_user_id": fields.Integer(required=True)})

