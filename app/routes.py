from flask import render_template, Blueprint, request, flash, session, redirect, url_for, abort
from app.models import Movie, User
from app import db
from uuid import uuid4
from dataclasses import asdict
from passlib.hash import pbkdf2_sha256
import time
import random
import bleach

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Recover movies from database
    movies = list(db.movies.find())
    return render_template('index.html', title="Movies Watchlist", movies=movies)


@main.route('/add_movie', methods=["POST"])
def add_movie():
    # User must be logged in to post movies.
    if 'current_user' not in session:
        flash('You must be logged in to post a new movie.')
        return redirect(url_for('main.login'))
    
    # Verify received form and clean suspicious information with bleach
    if request.method == "POST":
        cover = request.form.get('cover')
        title = request.form.get('title')
        director = request.form.get('director')
        genre = request.form.get('genre')
        subgenre = request.form.get('subgenre')
        description = request.form.get('description')

        if not all([cover, title, director, genre]):
            flash('All fields are required.')
            return redirect(url_for('main.add_movie'))
        
        cover = bleach.clean(cover)
        title = bleach.clean(title)
        director = bleach.clean(director)
        genre = bleach.clean(genre)
        subgenre = bleach.clean(subgenre)
        description = bleach.clean(description)

        # if exists, cancel process
        movie_exists = db.movies.find_one({'title': title, "director": director})
        if movie_exists:
            flash('This move already exists in our database.')
            return redirect(url_for('main.index'))
        
        # Create new movie based on Movie model
        movie = Movie(
            _id = str(uuid4()),
            cover = cover,
            title = title,
            director = director,
            genre = genre,
            subgenre = subgenre,
            description = description
        )

        # Add on database
        try:
            db.movies.insert_one(asdict(movie))
            flash('Movie added successfully!')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash('An error ocurred while adding the move. Please try again later.')
            return redirect(url_for('main.index'))

    flash("You must be logged in to post a new movie")
    return redirect(url_for('main.login'))


@main.route('/register', methods=["POST", "GET"])
def register():
    # Receive register form, verifying all fields
    if request.method == "POST":
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([name, username, password, confirm_password]):
            flash('All fields are required.')
            return redirect(url_for('main.register'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.')
            return redirect(url_for('main.register'))

        if password != confirm_password:
            flash('Both password must be equal.')
            return redirect(url_for('main.register'))
        
        user_exists = db.users.find_one({"username": username})

        if user_exists:
            flash('Login already exists, please choose another username')
            return redirect(url_for('main.register'))
        
        # Create User based on model and add on database if not exist
        try: 
            hashed_password = pbkdf2_sha256.hash(password)

            new_user = User(
            _id = str(uuid4()),
            name = name,
            username = username,
            password = hashed_password
            ) 

            db.users.insert_one(asdict(new_user))

            flash('Registration successfull. Please log in.')
            return redirect(url_for('main.login'))
        
        except Exception as e:
            flash('An error ocurred, please try again later.')
            print(e)
            return redirect(url_for('main.register'))

    return render_template('register.html', title="Movies Watchlist - Register")


@main.route('/login', methods=["POST", "GET"])
def login():
    if 'current_user' in session:
        flash("You're already logged in.")
        return redirect(url_for('main.index'))
    
    # Receive and login user using flask session if credentials correct
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('All fields are required.')
            return redirect(url_for('login'))

        time.sleep(random.uniform(0.2, 0.8))

        user = db.users.find_one({'username': username})
    

        if user and pbkdf2_sha256.verify(password, user['password']):
            flash('Log in succesfully')
            session['current_user'] = user['username']
            return redirect(url_for('main.index'))

        flash('Invalid credentials. Please try again.')
        return redirect(url_for('main.login'))
        
    return render_template('login.html', title="Movies Watchlist - Login")


@main.route('/logout')
def logout():
    session.pop('current_user')
    flash("You've logged out successfully")
    return redirect(url_for('main.index'))


@main.route('/movie_details/<_id>')   
def movie_details(_id):
    # Load movies from database based on id 
    clicked_movie = db.movies.find_one({"_id": _id})
    if not clicked_movie:
        abort(404, description="Movie not found")
    
    # Instance of Movie object with all methods, based on clicked_movie
    movie = Movie(**clicked_movie)

    # Movie object method for recalculate the average rating
    active_stars = int(movie.rating)

    # Recovering the number of ratings
    num_ratings = movie.num_ratings

    return render_template('movie_details.html', 
                           title=clicked_movie['title'], 
                           movie=clicked_movie, 
                           active_stars=active_stars, 
                           num_ratings = num_ratings)


@main.route('/rate_movie/<_id>', methods=["POST"])
def rate_movie(_id):
    # Verifiy if the user is logged in
    user = session.get('current_user')
    if not user:
        flash("You must be logged in to rate a movie.")
        return redirect(url_for('main.login'))
    
    current_user = db.users.find_one({'username': user})
    # Verifiy the star clicked
    rating = request.form.get('rating')

    if _id in current_user.get('rated_movies', []):
        flash("You've already rated this movie.")
        return redirect(url_for('main.movie_details', _id=_id))

    try:
        # Capture the submited value of the star and applies to rating of the user, between 1 and 5
        rating = int(rating)
        if not (1 <= rating <= 5):
            raise ValueError
    except ValueError:
        flash("Invalid rating value.")
        return redirect(url_for('main.movie_details', _id=_id))

    # Find the movie
    clicked_movie = db.movies.find_one({"_id": _id})
    if not clicked_movie:
        flash("Movie not found.")
        return redirect(url_for('main.index'))

    # Update movie with the new rating
    movie = Movie(**clicked_movie)
    movie.add_rating(rating)
    
    db.movies.update_one({"_id": _id}, {"$set": {"rating": movie.rating, "num_ratings": movie.num_ratings}})
    db.users.update_one({"username": user}, {"$push": {"rated_movies": _id}})
    flash("Rating submitted successfully!")
    return redirect(url_for('main.movie_details', _id=_id))


@main.route('/add_to_my_movies/<_id>')
def add_to_my_movies(_id):
    # Verify if user is logged in
    if not 'current_user' in session:
        flash('You must be logged in to add a movie to your list.')
        return redirect(url_for('main.login'))
    
    user = session.get('current_user')
    
    # Search and verify if movie exists in database
    movie_to_add = db.movies.find_one({'_id': _id})
    if not movie_to_add:
        flash('Movie not found.')
        return redirect(url_for('main.home'))

    if user:
        current_user = db.users.find_one({'username': user})

        # If movie is already in list, don't add
        if _id in current_user.get('watched_movies', []):
            flash('This movie is already in your list.')
            return redirect(url_for('main.movie_details', _id=_id))
        
        # Add only the movie's _id to the watched_movies array of the user
        db.users.update_one(
            {'username': current_user['username']},
            {'$push': {'watched_movies': _id}}  # Adding only the _id of the movie
        )

        flash('Movie added successfully to your list!')
        return redirect(url_for('main.movie_details', _id=_id))



@main.route('/my_movies/<username>')
def my_movies(username):
    # Verify if user is logged in
    if not 'current_user' in session:
        flash('You must be logged in to see your list')
        return redirect(url_for('main.login'))
    
    # Recover current user from database
    user = db.users.find_one({'username': username})
    if not user:
        flash('User not found.')
        return redirect(url_for('main.index'))
    
    # Recover watched movies array from user database
    watched_movies = user.get('watched_movies', [])

    # Initial empty array for append movies finded
    movies_details = []

    # Verify every movie in user array and append to list
    for _id in watched_movies:
        movie = db.movies.find_one({"_id": _id})
        if movie:
            movies_details.append(movie)
    
    return render_template('my_movies.html', title=f"My movies", movies_details=movies_details)