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
import random

app = Flask(__name__)
app.secret_key = os.environ['SECRETKEY']
MAPS_KEY = os.environ['MAPS_KEY']
GEO_PLACES_KEY = os.environ['GEO_PLACES_KEY']
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

    state_list = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]
    full_state_list = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
        'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
        'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
        'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
        'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 
        'Wisconsin', 'Wyoming'
    ]
    restaurant_state_dict = {}

    for idx, state in enumerate(state_list):
        # restaurant_state currently returns full 'City, ST'
        restaurant_state_dict[state] = {}
        filtered_restaurants = crud.get_states_restaurants(state)
        restaurant_state_dict[state][full_state_list[idx]] = filtered_restaurants


    # Need to duplicate this block on the html jinja side to store in accordions
    # sorted_restaurants = sorted(restaurant_state_dict)
    # print(sorted_restaurants)
    for state in sorted(restaurant_state_dict):
        print(f'State: {state}')
        long_state = list(restaurant_state_dict[state].keys())[0]
        print(f'Long State: {long_state}')
        print(f'Restaurants: {restaurant_state_dict[state][long_state]}')
    # pprint(restaurant_state_dict)

    return render_template('restaurants.html', restaurants=restaurants, MAPS_KEY=MAPS_KEY, sorted=sorted, list=list, restaurant_state_dict=restaurant_state_dict)

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
        award_badge = crud.award_badge(session['email'], 12)
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
            # trip = crud.get_trip_by_id(session["trip_id"])
            # restaurants = crud.get_restaurants()
            # user = crud.get_user_by_email(session["email"])

            return redirect('/edit-trip')
        else:
            flash("Please select a trip!")
            return redirect('/edit-trips')
    else:
        flash("Trying Real Sneaky Beaky Like, ey? You need to be logged in to do that!")
        return redirect('/')
    
@app.route('/edit-trip')
def edit_trip_page():

    if "email" in session:
        # if request.form.get("edit_trip"):
            # session["trip_id"] = int(request.form.get("edit_trip"))
        trip = crud.get_trip_by_id(session["trip_id"])
        restaurants = crud.get_restaurants()
        user = crud.get_user_by_email(session["email"])

        return render_template('edit_trip.html', trip=trip, restaurants=restaurants, user=user, MAPS_KEY=MAPS_KEY, pformat=pformat)

    else:
        flash("Trying Real Sneaky Beaky Like, ey? You need to be logged in to do that!")
        return redirect('/')
    
@app.route('/edit-trip-remove-stops', methods=["POST"])
def remove_stops():

    if "email" in session:
        remove_stop_restaurant_ids = request.form.getlist("remove_stops")
        crud.remove_stops(remove_stop_restaurant_ids, session["trip_id"])

        return redirect('/edit-trip')
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

        return redirect('/edit-trip')
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

    users = crud.get_users()
    return render_template('all_badges.html', users=users)

# This route likely to be removed. Makes more sense for user to be able to enter
#   their own starting address as a starting point
@app.route("/start-point-select.json") 
def start_point_select():

    if "email" in session:        
        start_restaurant_id = request.args.get("restaurantId")
        session['start_restaurant_id'] = start_restaurant_id
        print(start_restaurant_id)

        start_restaurant = crud.get_one_restaurant_by_id(start_restaurant_id)
        start_restaurant_address = start_restaurant.restaurant_address

        return start_restaurant_address
    else:
        flash("Please log in or crete an account for directions!")
        return "user not logged in"
    
@app.route("/end-point-select.json")
def end_point_select():

    if "email" in session:        
        end_restaurant_id = request.args.get("restaurantId")
        session['end_restaurant_id'] = end_restaurant_id
        print(end_restaurant_id)

        end_restaurant = crud.get_one_restaurant_by_id(end_restaurant_id)
        end_restaurant_address = end_restaurant.restaurant_address

        return end_restaurant_address
    else:
        flash("Please log in or crete an account for directions!")
        return "user not logged in"
    

@app.route('/api/direction-stops')
def direction_stop_info():
    """Return stops info with proper start and end from db in JSON form for Directions API"""
    
    if 'email' in session:
        if 'user_address' in session and 'end_restaurant_id' in session:
            stops = []
            trip = crud.get_trip_by_id(session["trip_id"])

            start_address = session['user_address']
            end = crud.get_one_restaurant_by_id(session['end_restaurant_id'])

            stops.append({
                        "restaurant_id" : "User Address Start Point",
                        "restaurant_name" : "User Address Start Point",
                        "restaurant_icon" : "User Address Start Point",
                        "restaurant_description" : "User Address Start Point",
                        "restaurant_address" : start_address,
                        "restaurant_latitude" :"User Address Start Point",
                        "restaurant_longitude" : "User Address Start Point",
                        "restaurant_state" : "User Address Start Point",
                        "food_type" : "User Address Start Point",
                        "episode_info" : "User Address Start Point"
                    })

            for restaurant in trip.restaurants:
                if restaurant != end:
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

            stops.append({
                        "restaurant_id" : end.restaurant_id,
                        "restaurant_name" : end.restaurant_name,
                        "restaurant_icon" : end.restaurant_icon,
                        "restaurant_description" : end.restaurant_description,
                        "restaurant_address" : end.restaurant_address,
                        "restaurant_latitude" : end.restaurant_latitude,
                        "restaurant_longitude" : end.restaurant_longitude,
                        "restaurant_state" : end.restaurant_state,
                        "food_type" : end.food_type,
                        "episode_info" : end.episode_info
                    })

            # Throw an error in dev console if the order doesn't get done correctly after selecting new start/end
            if stops[0]['restaurant_address'] != start_address:
                return "error when ordering direction start point"
            elif stops[len(stops)-1]['restaurant_id'] != end.restaurant_id:
                return "error when ordering direction end point"

            return jsonify(stops)
        
        else:
            stops = []

            return jsonify(stops)
    
    else:
        flash("You shouldn't be here!")
        # Would this redirect even work?
        return redirect('/')
    
@app.route('/route-to-maps.json')
def route_to_maps():

    if 'email' in session:

        orderedStops = request.args.get('orderedStops')
        trip = crud.get_trip_by_id(session["trip_id"])

        if 'user_address' in session and 'end_restaurant_id' in session:
            
            start_address = session['user_address']
            end = crud.get_one_restaurant_by_id(session['end_restaurant_id'])

            print(start_address)
            print(orderedStops)
            print(end)
            print('********')

            param_address = crud.make_maps_param(start_address, end, orderedStops)
                    
            print(param_address)

            # return redirect(f'https://www.google.com/maps/dir/?api=1&{param_address}')
            return param_address
        
        else:
            return 'Please first submit "Get Directions"'
    else:
            return 'Please login'
        
@app.route('/new-user-address.json')
def new_user_address():

    if 'email' in session:

        print("made it to app route")

        new_user_address = request.args.get('newUserAddress')

        geocoded_user_address = crud.convert_address_to_geocode(new_user_address)

        if geocoded_user_address == 'INVALID_REQUEST':
            print('in this if loop')
            return "Entered address not valid, please try again."
        elif geocoded_user_address == 'ZERO_RESULTS':
            print('in this if loop')
            return "Entered address not valid, please try again."

        formatted_address = crud.get_formatted_address(geocoded_user_address)

        session['user_address'] = formatted_address

        return formatted_address
    
    else:
        flash("Please log in or create an account for directions!")
        return "user not logged in"

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)