"""Association table between two classes film_genre"""

from filmapp import db


class Filmgenre(db.Model):
    __tablename__ = 'filmgenre'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey("film.id"))
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))

    def __init__(self, film_id, genre_id):
        self.film_id = film_id
        self.genre_id = genre_id
