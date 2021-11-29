import pytest
from filmapp import app
# from film_genre import Filmgenre
# from film_director import Filmdirector
# from film import Film
# from user import User
# from genre import Genre
# from director import Director

@pytest.fixture
def client():
    """Testing app"""
    app_for_test = app.test_client({'TESTING': True})
    with app_for_test as client:
        yield client

# @pytest.fixture
# def login_user(client):
#     user = client.post("/login", data={"nickname": Gagarin, "password": 66666})
#     return user

def test_get(client):
    response = client.get('/')
    print(response)
#
#
def test_login(client):
    print(client)
    response = client.post("/login", data={"nick": "Admin", "password": "123"})
    print(response)


def test_s(client):
    print(client)
    response = client.get("/films-api/Searc")
    print(response)