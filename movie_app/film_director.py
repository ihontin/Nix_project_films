"""Association table between two classes film_director"""

from app import db


class Filmdirector(db.Model):
    __tablename__ = 'filmdirector'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey("film.id"))
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))

    def __init__(self, film_id, director_id):
        self.film_id = film_id
        self.director_id = director_id
