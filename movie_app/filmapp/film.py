"""Main table Film"""

from flask_restx import fields
from filmapp import db, api
# from movie_app.models.film_director import Filmdirector
# from movie_app.models.film_genre import Filmgenre


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

# class FilmSchema(ma.SQLAlchemySchema):
#     class Meta:
#         fields = ("title", "release", "poster", "rating", "description", "fk_user_id")
        # model = Film


# one_field = FilmSchema()
# many_fields = FilmSchema(many=True)
