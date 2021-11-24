"""Routes and function to all models"""
from app import db, api, login_manager, app
from flask import jsonify, abort, redirect, url_for
from flask_restx import Resource, reqparse
from film_genre import Filmgenre
from film_director import Filmdirector
from film import Film, model_film
from user import User, model_user
from genre import Genre
from director import Director
import datetime
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash


@api.route('/')
class RootPage(Resource):
    """Root page"""

    # @api.doc(body=user_login_resource)
    @api.marshal_with(model_user, code=200, envelope="user")
    def get(self):
        return {'Hello': 'World'}


@login_manager.user_loader
def load_user(id):
    """ User in session """
    return db.session.query(User).get(id)


@api.route('/login')
class LogPage(Resource):
    """Post method for login"""

    @api.marshal_with(model_user, code=200, envelope="user")
    def post(self):
        """Post login method"""
        parser = reqparse.RequestParser()
        parser.add_argument('nick', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        user_log = db.session.query(User).filter(User.login == args['nick']).first()
        user_pass = False
        if user_log:
            user_pass = check_password_hash(user_log.password, str(args['password']))
        if user_pass:
            login_user(user_log, remember=True, duration=datetime.timedelta(days=2))
            return {"id": current_user.id,
                    "login": current_user.login,
                    "password": current_user.password,
                    "admin": current_user.admin}
        return abort(403, "Nickname or password not correct")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('root_page'))


@app.after_request
def redirect_to_signin(response):
    """Redirect to LogPage"""
    if response.status_code == 401:
        return redirect(url_for('log_page'))
    return response


@api.route('/register/')
class Register(Resource):
    """Post method for login"""

    # @api.doc(body=user_login_resource)
    @api.marshal_with(model_user, code=200, envelope="user")
    def post(self):
        """Add new user"""
        parser = reqparse.RequestParser()
        parser.add_argument('nick', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('password2', type=str, required=True)
        args = parser.parse_args()
        exist_nitck = db.session.query(User).filter(User.login == args['nick']).first()
        if exist_nitck is not None:
            abort(403, f"User with nickname {args['nick']} already exists. Login should be unique")
        if not (args['nick'] and args['password'] and args['password2']):
            abort(403, description="All fields must be filled")
        if args['password'] != args['password2']:
            abort(406, description="Passwords should be equal")
        if len(args['nick']) <= 4 or len(args['password']) <= 4:
            abort(406, description="Passwords and nick should be at least five characters long")
        elif len(args['nick']) > 4 and len(args['password']) > 4:
            pass_hash = generate_password_hash(args['password'])
            new_user = User(login=args['nick'], password=pass_hash, admin=0)
            db.session.add(new_user)
            db.session.commit()
            if new_user:
                return {"id": current_user.id,
                        "login": current_user.login,
                        "password": current_user.password,
                        "admin": current_user.admin}

        return abort(403, "Nickname or password not correct")


def film_sort_def(operation, pagin):
    """Sorting films"""
    if operation == 'by_title':
        var = db.session.query(Film).order_by(Film.title).paginate(page=pagin).items
        return var
    elif operation == 'rating':
        var = db.session.query(Film).order_by(Film.rating).paginate(page=pagin).items
        return var
    elif operation == 'release':
        var = db.session.query(Film).order_by(Film.release).paginate(page=pagin).items
        return var


@api.route('/films-api/Sort-Searc')
class SortFilms(Resource):
    """Sorting films by: release, rating and by_title by default"""

    @login_required
    @api.marshal_with(model_film, code=200, envelope="film")
    def get(self):
        """Choose operation and sorting films"""
        parser = reqparse.RequestParser()
        parser.add_argument('pagination', type=int, default=1)
        parser.add_argument('operation', type=str, default='by_title')
        args = parser.parse_args()
        res = film_sort_def(args['operation'], args['pagination'])
        return res


def search_by_operation(text, operation, pagin, lower_year, upper_year):
    """serching films"""
    if operation == 'none':
        return "Len should be more then 1 symbol", 400
    elif operation == 'director':
        if search_empty_fields(text):
            search = "%{}%".format(text)
            search_last_name = Film.query.join(Film.fk_director_id). \
                filter(Director.last_name.like(search)).paginate(page=pagin).items
            if search_last_name:
                return search_last_name
            return "Films not found", 404
        return "Len should be more then 1 symbol", 400
    elif operation == 'genre':
        if search_empty_fields(text):
            search_genre = Film.query.join(Film.fk_genre_id). \
                filter(Genre.title.like(text)).paginate(page=pagin).items
            if search_genre:
                return search_genre
            return "Films not found", 404
        return "Len should be more then 1 symbol", 400
    elif operation == 'relisedate':
        search_relisedate = Film.query.filter(
            Film.release > lower_year + '-01-01',
            Film.release < upper_year + '-12-31').paginate(page=pagin).items
        if search_relisedate:
            return search_relisedate
        return "Films not found", 404


def search_empty_fields(text):
    """If fields are empty, return - 404"""
    if len(text) == 0:
        return False
    elif len(text) < 2:
        return False
    return True


@api.route('/films-api/Searc')
class SearchFilms(Resource):
    """Search by: genre, director, relisedate"""

    @login_required
    @api.marshal_with(model_film, code=200, envelope="film")
    def get(self):
        """Choose operation and searching films"""
        upper_year = str(datetime.datetime.now().year)
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, default='none')
        parser.add_argument('operation', type=str, default='none')
        parser.add_argument('pagination', type=int, default=1)
        parser.add_argument('lower_year', type=str, default='1900')
        parser.add_argument('upper_year', type=str, default=upper_year)
        args = parser.parse_args()
        res = search_by_operation(args['text'], args['operation'],
                                  args['pagination'], args['lower_year'], args['upper_year'])
        return res


def chosen_sort(chosen):
    """Choose kind of sorting for search"""
    sort_var = Film.title
    if chosen == "rating":
        sort_var = Film.rating
    elif chosen == "release":
        sort_var = Film.release
    return sort_var


def search_operation_sort_rating(text, operation, ascending,
                                 pagin, lower_year, upper_year, sorting_by):
    """Serching films, sort by rating
    descending by defoult"""
    sort_variable = chosen_sort(sorting_by)
    if operation == 'none':
        return "Len should be more then 1 symbol", 400
    elif operation == 'director':
        if search_empty_fields(text):
            search = "%{}%".format(text)
            if ascending == 'ascending':
                search_last_name = Film.query.join(Film.fk_director_id). \
                    filter(Director.last_name.like(search)) \
                    .order_by(sort_variable).paginate(page=pagin).items
            else:
                search_last_name = Film.query.join(Film.fk_director_id). \
                    filter(Director.last_name.like(search)). \
                    order_by(db.desc(sort_variable)).paginate(page=pagin).items
            if search_last_name:
                return search_last_name
            return "Films not found", 404
        return "Len should be more then 1 symbol", 400
    elif operation == 'genre':
        if search_empty_fields(text):
            if ascending == 'ascending':
                search_genre = Film.query.join(Film.fk_genre_id) \
                    .filter(Genre.title.like(text)).order_by(sort_variable) \
                    .paginate(page=pagin).items
            else:
                search_genre = Film.query.join(Film.fk_genre_id) \
                    .filter(Genre.title.like(text)).order_by(db.desc(sort_variable)) \
                    .paginate(page=pagin).items
            if search_genre:
                return search_genre
            return "Films not found", 404
        return "Len should be more then 1 symbol", 400
    elif operation == 'relisedate':
        if ascending == 'ascending':
            search_relisedate = Film.query.filter(
                Film.release > lower_year + '-01-01',
                Film.release < upper_year + '-12-31') \
                .order_by(sort_variable) \
                .paginate(page=pagin).items
        else:
            search_relisedate = Film.query.filter(
                Film.release > lower_year + '-01-01',
                Film.release < upper_year + '-12-31').order_by(db.desc(sort_variable)) \
                .paginate(page=pagin).items
        if search_relisedate:
            return search_relisedate
        return "Films not found", 404


# .order_by(Film.rating)

@api.route('/films-api/Search-reting-Sort')
class SortRetingSearchFilms(Resource):
    """Searching films by genre, director, relisedate, sort by rating"""

    @login_required
    @api.marshal_with(model_film, code=200, envelope="film")
    def get(self):
        """Choose operation and searching films"""
        upper_year = str(datetime.datetime.now().year)
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, default='none')  # arg for director and genre
        parser.add_argument('operation', type=str, default='none')  # search by genre, director, relisedate
        parser.add_argument('pagination', type=int, default=1)
        parser.add_argument('lower_year', type=str, default='1900')
        parser.add_argument('upper_year', type=str, default=upper_year)
        parser.add_argument('ascending', type=str, default='descending')  # kind of sort
        parser.add_argument('sorting_var', type=str, default='')  # rating or release
        args = parser.parse_args()
        res = search_operation_sort_rating(args['text'], args['operation'], args['ascending'],
                                           args['pagination'], args['lower_year'],
                                           args['upper_year'], args['sorting_var'])
        return res


@api.route('/films-api/update_film')
class UpdateFilms(Resource):
    """Serching films by genre, director, relisedate, sort by rating"""

    @login_required
    @api.marshal_with(model_film, code=200, envelope="film")
    def post(self):
        ...

# should find many dirictors
# search_last_name = db.session.query(Film, Director) \
#     .join(Director, Director.director_id == Film.film_id)\
#     .filter(Director.last_name.like(search)).paginate(page=pagin).items
# if search_last_name:
#     list_searsh, count = {}, 0
#     for i in search_last_name:
#         count += 1
#         for j in i:
#             if isinstance(j, Film):
#                 list_searsh[count]= {"film_id" : j.film_id}
#                 list_searsh[count]["title"] = j.title
#                 list_searsh[count]["release"] = j.release
#                 list_searsh[count]["poster"] = j.poster
#                 list_searsh[count]["rating"] = j.rating
#                 list_searsh[count]["description"] = j.description
#             else:
#                 list_searsh[count]["director_first_name"] = j.first_name
#                 list_searsh[count]["director_last_name"] = j.last_name
#         list_searsh[count] = list(list_searsh[count])
#     print(list_searsh)
#     return jsonify(list_searsh)
