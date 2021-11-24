"""Main table Film"""

from flask_restx import fields
from app import db, ma, api
from film_director import Filmdirector
from film_genre import Filmgenre


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    release = db.Column(db.Date(), nullable=False)
    poster = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    fk_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    fk_director_id = db.relationship('Director', secondary='filmdirector',
                                     back_populates="fk_filmdir_id")
    fk_genre_id = db.relationship('Genre', secondary='filmgenre',
                                  back_populates="fk_filmgen_id")

    def __init__(self, title, release, poster, rating, description, fk_user_id):
        self.title = title
        self.release = release
        self.poster = poster
        self.rating = rating
        self.description = description
        self.fk_user_id = fk_user_id


model_film = api.model(
    "Film", {
        "id": fields.Integer(required=True),
        "title": fields.String(required=True),
        "release": fields.Date(required=True),
        "poster": fields.String(required=True),
        "rating": fields.Integer(required=True),
        "description": fields.String(required=False),
        "fk_user_id": fields.Integer(required=True)})


class FilmSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("title", "release", "poster", "rating", "description", "fk_user_id")
        # model = Film


one_field = FilmSchema()
many_fields = FilmSchema(many=True)
