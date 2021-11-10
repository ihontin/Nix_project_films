"""Creation and filling database Films library"""
import json
from app import db


# import all models
from film_genre import film_genre
from film_director import film_director
from film import Film
from user import User
from genre import Genre
from director import Director


def seeding_db():
    result = db.session.query(Director).all()

    if len(result) == 0:
        directors_list, genre_list, film_list = [], [], []
        # Fill DIRECTOR Table
        with open("./data/director.json", 'r', encoding='utf-8') as dir_file:
            json_direct = json.load(dir_file)

        for row in json_direct:
            fill_direct = Director(first_name=row['first_name'], last_name=row['last_name'])
            directors_list.append(fill_direct)
            db.session.add(fill_direct)

        # Fill GENRE Table
        with open("./data/genre.json", 'r', encoding='utf-8') as gen_file:
            json_genre = json.load(gen_file)

        for row in json_genre:
            fill_genre = Genre(genre_id=row['genre_id'], title=row['title'])
            genre_list.append(fill_genre)
            db.session.add(fill_genre)

        # Fill USER Table
        with open("./data/user.json", 'r', encoding='utf-8') as user_file:
            json_user = json.load(user_file)

        for row in json_user:
            fill_user = User(id=row['id'], login=row['login'],
                             password=row['password'])
            db.session.add(fill_user)

        # Fill FILM Table
        with open("./data/film.json", 'r', encoding='utf-8') as film_file:
            json_film = json.load(film_file)

        for row in json_film:
            fill_film = Film(film_id=row['film_id'], title=row['title'],
                             release=row['release'], poster=row['poster'], rating=row['rating'],
                             description=row['description'], fk_user_id=row['fk_user_id'])
            film_list.append(fill_film)
            db.session.add(fill_film)

        # Fill FILM_director Table
        for i in range(len(film_list)):
            directors_list[i].filmdir.append(film_list[i])

        # Fill FILM_genre Table
        genre_list[11].filmgen.append(film_list[0])
        genre_list[0].filmgen.append(film_list[0])
        genre_list[5].filmgen.append(film_list[1])
        genre_list[0].filmgen.append(film_list[1])
        genre_list[0].filmgen.append(film_list[2])
        genre_list[1].filmgen.append(film_list[3])
        genre_list[0].filmgen.append(film_list[3])
        db.session.commit()
    else:
        print("The database is seeded")
        db.session.commit()


