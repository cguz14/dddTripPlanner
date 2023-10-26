"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
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
MAPS_KEY = os.environ['MAPS_KEY']
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """Show homepage"""

    # The way you did this was dirty, ask if there are more kosher ways to perform this update without seed
    # crud.add_guy_default()

    return render_template('homepage.html')

@app.route('/restaurants')
def show_restaurants():
    """Shows all restaurants"""

    restaurants = crud.get_restaurants()

    return render_template('restaurants.html', restaurants=restaurants, MAPS_KEY=MAPS_KEY)

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
        user = crud.get_user_by_email(session['email'])
        return render_template("profile.html", user=user)
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
    elif username == "" or password == "" or email == "":
        flash("Please enter account information")
        return redirect("/new-account")
    else:
        user = crud.create_user(username, email, password, user_icon)
        db.session.add(user)
        db.session.commit()
        session["username"] = username
        session["email"] = email
        session["user_id"] = user.user_id
        session["user_icon"] = user_icon
        award_badge = crud.award_badge(session['email'], 'accountCreate')
        flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')

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
        user = crud.get_user_by_email(session['email'])
        ratings = crud.get_ratings(user)
        rating_restaurant_ids = crud.get_rating_restaurant_ids(ratings)
        return render_template('favorites.html', favorites=favorites, rating_restaurant_ids=rating_restaurant_ids)
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

        if not crud.check_for_badge(session['email'], 14):
            award_badge = crud.award_badge(session['email'], 14)
            flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')
        
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

        return render_template("trips.html", trips=trips)
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

        # Award First Trip badge if badge not already awarded
        if not crud.check_for_badge(session['email'], 11):
            award_badge = crud.award_badge(session['email'], 11)
            flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')
        
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
    
@app.route('/edit-trips')
def edit_trips_page():

    if "email" in session:
        trips = crud.get_trips(session["email"])

        if trips:
            return render_template('edit_trips.html', trips=trips)
        else:
            flash('You have no trips to edit! Use "Create new trip" button to start your journey!')
            return redirect('/trips')
    else:
        flash("You need to be logged in to do that!")
        return redirect('/')
    
@app.route('/edit-trip', methods=["POST"])
def edit_trip():

    if "email" in session:
        if request.form.get("edit_trip"):
            session["trip_id"] = int(request.form.get("edit_trip"))
            trip = crud.get_trip_by_id(session["trip_id"])
            restaurants = crud.get_restaurants()
            user = crud.get_user_by_email(session["email"])

            return render_template('edit_trip.html', trip=trip, restaurants=restaurants, user=user, MAPS_KEY=MAPS_KEY, pformat=pformat)
        else:
            flash("Please select a trip!")
            return redirect('/edit-trips')
    else:
        flash("Trying Real Sneaky Beaky Like, ey? You need to be logged in to do that!")
        return redirect('/')
    
@app.route('/edit-trip-remove-stops', methods=["POST"])
def remove_stops():

    if "email" in session:
        remove_stop_restaurant_ids = request.form.getlist("remove_stops")
        crud.remove_stops(remove_stop_restaurant_ids, session["trip_id"])

        return redirect('/trips')
    else:
        flash("How'd you get there? You need to be logged in to do that!")
        return redirect('/')
    
@app.route('/edit-trip-add-stops', methods=["POST"])
def add_stops():

    if "email" in session:
        add_stop_restaurant_ids = request.form.getlist("add_stops")
        add_stop_restaurants = crud.get_restaurants_by_id(add_stop_restaurant_ids)
        crud.add_stops(add_stop_restaurants, session["trip_id"])
        trip = crud.get_trip_by_id(session["trip_id"])
        stops = crud.get_stops([trip])
        db.session.add_all(stops)
        db.session.commit()

        if not crud.check_for_badge(session['email'], 15):
            award_badge = crud.award_badge(session['email'], 15)
            flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')

        return redirect('/trips')
    else:
        flash("Stop trying to h4ck the syst3m. You need to be logged in to access!")
        return redirect('/')
    
@app.route('/change-trip-name.json')
def change_trip_name():

    if "email" in session:
        new_trip_name = request.args.get("newTripName")
        trip = crud.get_trip_by_id(session["trip_id"])
        trip.trip_name = new_trip_name
        db.session.commit()

        if not crud.check_for_badge(session['email'], 15):
            award_badge = crud.award_badge(session['email'], 15)
            flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')
        
        return new_trip_name
    else:
        flash("Like the great Dikembe Mutombo once said... No, no, no! You need to log in.")
        return redirect('/')
    
@app.route('/change-trip-description.json')
def change_trip_description():

    if "email" in session:
        new_trip_description = request.args.get("newTripDescription")
        trip = crud.get_trip_by_id(session["trip_id"])
        trip.trip_description = new_trip_description
        db.session.commit()
        
        if not crud.check_for_badge(session['email'], 15):
            award_badge = crud.award_badge(session['email'], 15)
            flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')

        return new_trip_description
    else:
        flash("Tim Duncan with the BLOCK! You need to be logged in to access this.")
        return redirect('/')
    
@app.route('/change-username.json')
def change_username():

    if "email" in session:
        new_username = request.args.get("newUsername")
        if new_username == "":
            flash("Please enter a username")
            return redirect('/profile')
        
        user = crud.get_user_by_email(session["email"])
        session["username"] = new_username
        user.username = new_username
        db.session.commit()
        
        return new_username
    else:
        flash("Elliot for Three! You need to be logged in to access this.")
        return redirect('/')
    
@app.route('/api/restaurants')
def restaurant_info():
    """Return restaurant info from db in JSON form for Map API and other JS needs"""
    
    restaurants = []

    for restaurant in crud.get_restaurants():
        restaurants.append({
            "restaurant_id" : restaurant.restaurant_id,
            "restaurant_name" : restaurant.restaurant_name,
            "restaurant_icon" : restaurant.restaurant_icon,
            "restaurant_description" : restaurant.restaurant_description,
            "restaurant_address" : restaurant.restaurant_address,
            "restaurant_latitude" : restaurant.restaurant_latitude,
            "restaurant_longitude" : restaurant.restaurant_longitude,
            "restaurant_state" : restaurant.restaurant_state,
            "food_type" : restaurant.food_type,
            "episode_info" : restaurant.episode_info
        })

    return jsonify(restaurants)

@app.route('/api/stops')
def stop_info():
    """Return restaurant info from db in JSON form for Map API and other JS needs"""
    
    stops = []
    trip = crud.get_trip_by_id(session["trip_id"])

    for restaurant in trip.restaurants:
        stops.append({
            "restaurant_id" : restaurant.restaurant_id,
            "restaurant_name" : restaurant.restaurant_name,
            "restaurant_icon" : restaurant.restaurant_icon,
            "restaurant_description" : restaurant.restaurant_description,
            "restaurant_address" : restaurant.restaurant_address,
            "restaurant_latitude" : restaurant.restaurant_latitude,
            "restaurant_longitude" : restaurant.restaurant_longitude,
            "restaurant_state" : restaurant.restaurant_state,
            "food_type" : restaurant.food_type,
            "episode_info" : restaurant.episode_info
        })

    return jsonify(stops)

@app.route('/api/favorites')
def favorite_info():
    """Return restaurant info from db in JSON form for Map API and other JS needs"""
    
    favorites = []

    for restaurant in crud.get_favorites(session['email']):
        favorites.append({
            "restaurant_id" : restaurant.restaurant_id,
            "restaurant_name" : restaurant.restaurant_name,
            "restaurant_icon" : restaurant.restaurant_icon,
            "restaurant_description" : restaurant.restaurant_description,
            "restaurant_address" : restaurant.restaurant_address,
            "restaurant_latitude" : restaurant.restaurant_latitude,
            "restaurant_longitude" : restaurant.restaurant_longitude,
            "restaurant_state" : restaurant.restaurant_state,
            "food_type" : restaurant.food_type,
            "episode_info" : restaurant.episode_info
        })

    return jsonify(favorites)

@app.route("/change-likes.json")
def change_likes():
    
    if "email" in session:        
        restaurant_id = request.args.get("restaurantId")
        liked = request.args.get("liked")
        if liked == "true":
            liked = True
        else:
            liked = False

        user = crud.get_user_by_email(session["email"])
        crud.change_like(liked, user, restaurant_id)

        if not crud.check_for_badge(session['email'], 13):
            award_badge = crud.award_badge(session['email'], 13)
            flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')

        if len(user.ratings) > 9:
            if not crud.check_for_badge(session['email'], 16):
                award_badge = crud.award_badge(session['email'], 16)
                flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')

        if len(user.ratings) > 49:
            if not crud.check_for_badge(session['email'], 17):
                award_badge = crud.award_badge(session['email'], 17)
                flash(f'"{award_badge.badge_name}" Badge Awarded! {award_badge.badge_description}')

        return "app route completed"
        # getting restaurant name, need id and userid for new favorite.
        # restaurant_id = crud.get 
        # need to create favorite if user likes/dislikes and apply t/f depending
        # what if anything needs to be returned to the js/html side?
    else:
        flash("Please log in or crete an account to save ratings.")
        return "user not logged in"
    
@app.route('/api/ratings.json')
def rating_info():
    """Return rating info from db in JSON form for like/dislike javascript"""
    
    sent_ratings = []
    print('made it here')

    if 'email' in session:
        user = crud.get_user_by_email(session["email"])
        # favorites = crud.get_favorites(session["email"])
        ratings = crud.get_ratings(user)

        for rating in ratings:
            sent_ratings.append({
                "rating_id" : rating.rating_id,
                "thumbs_up" : rating.thumbs_up,
                "rating_icon" : rating.rating_icon,
                "user_id" : rating.user_id,
                "restaurant_id" : rating.restaurant_id,
            })

    return jsonify(sent_ratings)

@app.route('/all-badges')
def show_all_badges():
    """For dev purposes only. Show all badges that have been awarded"""

    badges = crud.get_all_badges()
    return render_template('all_badges.html', badges=badges)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)