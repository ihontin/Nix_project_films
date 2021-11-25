"""Start module"""
from flask_migrate import Migrate
from flask_script import Manager

from app import app, db
import routes

manager = Manager(app)
migrate = Migrate(app, db)

from film_genre import Filmgenre
from film_director import Filmdirector
from film import Film
from user import User
from genre import Genre
from director import Director


@manager.command
def creation():
    """Database creation"""
    from manage import create_db
    create_db()


@manager.command
def seeding():
    """Seeding database"""
    from manage import seeding_db
    seeding_db()


if __name__ == "__main__":
    app.run(debug=True)
    # manager.run()
