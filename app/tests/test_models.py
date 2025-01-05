import pytest
from ...app.models import User, Movie
from ...app import db

# Testing the User model
def test_user_model():
    # Creating a new user with the username "testuser" and password "testpassword"
    user = User(username="testuser", password="testpassword")
    
    # Inserting the user into the database as a dictionary
    db.users.insert_one(user.to_dict())

    # Finding the user in the database by username
    found_user = db.users.find_one({"username": "testuser"})
    
    # Asserting that the user was found and the username is correct
    assert found_user is not None
    assert found_user['username'] == 'testuser'

# Testing the Movie model
def test_movie_model():
    # Creating a new movie with specified details
    movie = Movie(
        _id="1234",
        cover="http://linkdaimagem.com",
        title="Inception",
        director="Christopher Nolan",
        genre="Sci-Fi",
        subgenre="Thriller",
        description="A mind-bending thriller."
    )
    
    # Inserting the movie into the database as a dictionary
    db.movies.insert_one(movie.to_dict())

    # Finding the movie in the database by title
    found_movie = db.movies.find_one({"title": "Inception"})
    
    # Asserting that the movie was found and the title is correct
    assert found_movie is not None
    assert found_movie['title'] == "Inception"
