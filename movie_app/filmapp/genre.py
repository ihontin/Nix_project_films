"""Table Genre"""
from filmapp import db
# from movie_app.models.film_genre import Filmgenre

class Genre(db.Model):
    """Create genre class"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(15), nullable=True)
    fk_filmgen_id = db.relationship('Film', secondary='filmgenre',
                                 back_populates="fk_genre_id")


    def __init__(self, title):
        self.title = title




