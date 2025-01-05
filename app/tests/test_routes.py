import pytest
from ...app import create_app, db
from app.models import User, Movie
from flask import session
from dataclasses import asdict

@pytest.fixture
def app():
    # Create flask and db instance for tests
    app = create_app(testing=True)
    yield app

@pytest.fixture
def client(app):
    # Client for test http
    return app.test_client()

def test_login(client, db):
    # Register user
    user = User(username='testuser', password='testpassword')
    db.users.insert_one(asdict(user))

    # Try to login
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'Login successfully' in response.data

def test_add_movie(client, db):
    # Create a user
    user = User(username='testuser', password='testpassword')
    db.users.insert_one(user.to_dict())

    # User login
    client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})

    # Add a movie
    response = client.post('/add_movie', data={
        'cover': 'http://linkdaimagem.com',
        'title': 'Inception',
        'director': 'Christopher Nolan',
        'genre': 'Sci-Fi',
        'subgenre': 'Thriller',
        'description': 'A mind-bending thriller.'
    })
    assert response.status_code == 302  # Redirect after success 
    assert b'Movie added successfully!' in response.data

# Test logout
def test_logout(client, init_db):
    # Create user
    user = User(username='testuser', password='testpassword')
    db.users.insert_one(user.to_dict())

    # Login user
    client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})

    # Logout
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect after logout
    assert b"You've logged out successfully" in response.data