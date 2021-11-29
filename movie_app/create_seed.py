from library import app, db
import routes


from library.film_genre import Filmgenre
from library.film_director import Filmdirector
from library.film import Film
from library.user import User
from library.genre import Genre
from library.director import Director


def creation():
    """Database creation"""
    from manage import create_db
    create_db()


def seeding():
    """Seeding database"""
    from manage import seeding_db
    seeding_db()
    
