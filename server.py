"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
import crud
from model import connect_to_db, db, Restaurant, User, UsersBadge, Badge, Rating, Favorite, Trip, Stop
from pprint import pformat, pprint
from bs4 import BeautifulSoup as bs

from jinja2 import StrictUndefined

import os
import json
import requests

app = Flask(__name__)
app.secret_key = os.environ['SECRETKEY']
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """Show homepage"""

    return render_template('homepage.html')

@app.route('/restaurants')
def show_restaurants():
    """Shows all restaurants"""

    restaurants = crud.get_restaurants()

    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/login', methods=["POST"])
def user_login():
    """User Profile Page"""

    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if crud.is_user(email, password):
        session["email"] = email
        session["username"] = user.username
        session["user_id"] = user.user_id
        session["user_icon"] = user.user_icon
        return redirect("/profile")
    else:
        flash("Login info not found, please try again or create new account")
        return redirect("/")
    
@app.route('/profile')
def user_profile():
    """Users profile info"""

    if "email" in session:
        return render_template("profile.html")
    else:
        flash("You need to login first!")
        return redirect("/")
    

@app.route('/new-account', methods=["POST"])
def new_user():
    """New User create goes to profile page with added tutorial"""

    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    user_icon = "static/img/attachment-guys-diner-background.jpg"

    if crud.email_exists(email):
        flash("Email already exists, please use another email")
        return redirect("/new-account")
    else:
        user = crud.create_user(username, email, password, user_icon)
        db.session.add(user)
        db.session.commit()
        session["username"] = username
        session["email"] = email
        session["user_id"] = user.user_id
        session["user_icon"] = user_icon
        flash("You're on your way to FlavorTown!")

        return redirect('/profile')
   
@app.route('/new-account')
def create_account_page():
    
    return render_template('new_account.html')

@app.route('/all-users')
def all_users():

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route('/favorites')
def favorites():

    if "email" in session:
        favorites = crud.get_favorites(session["email"])
        return render_template('favorites.html', favorites=favorites)
    else:
        flash("You need to login first!")
        return redirect("/")
    
@app.route('/add-favorites', methods=["POST"])
def add_favorites():

    if "email" in session:
        new_favorites = request.form.getlist('restaurant')
        new_favorite_restaurants = crud.get_restaurants_by_id(new_favorites)

        crud.add_favorites(session["email"], new_favorite_restaurants)     
        favorites = crud.get_favorites(session["email"])
        db.session.add_all(favorites)
        db.session.commit()
        
        return redirect('/favorites')
    else:
        flash("You need to login first!")
        return redirect("/")
    
@app.route('/remove-favorites', methods=["POST"])
def remove_favorites():

    if "email" in session:
        remove_favorites = request.form.getlist('remove_favorite')
        crud.remove_favorites(session["email"], remove_favorites)     
        
        return redirect('/favorites')
    else:
        flash("You need to login first!")
        return redirect("/")
    
@app.route('/logout')
def logout():

    if "email" in session:
        session.clear()
        db.session.commit()
        flash("Successfully Logged out")
        return redirect('/')
    else:
        flash("You need to be logged in to do that!")
        return redirect('/')

@app.route('/trips')
def trips():

    if "email" in session:
        trips = crud.get_trips(session["email"])
        stops = crud.get_stops(trips)
        # is there a more efficient way to get the restaurant db to trips so I
        # can use the id given by stops to pull a restaurant name?
        restaurants = crud.get_stop_restaurants(stops)
        return render_template("trips.html", trips=trips, stops=stops, restaurants=restaurants)
    else:
        flash("You need to be logged in to do that!")
        return redirect('/')
    
@app.route('/create-trip')
def create_trip_page():

    if "email" in session:
        # favorites = crud.get_favorites(session["email"])
        return render_template('create_trip.html')
    else:
        flash("You need to be logged in to do that!")
        return redirect('/')
    
@app.route('/create-trip', methods=["POST"])
def add_new_trip():

    if "email" in session:
        trip_name = request.form.get("trip_name")
        trip_description = request.form.get("trip_description")
        new_trip = crud.create_trip(trip_name, trip_description, session["user_id"])
        crud.add_trip_to_db(new_trip)        

        return redirect('/trips')
    else:
        flash("You need to be logged in to do that!")
        return redirect('/')
    
@app.route('/remove-trips', methods=["POST"])
def remove_trip():

    if "email" in session:
        remove_trips = request.form.getlist('remove_trip')
        crud.remove_trips(session["email"], remove_trips)      

        return redirect('/trips')
    else:
        flash("You need to be logged in to do that!")
        return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)