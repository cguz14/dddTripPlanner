from model import connect_to_db, db, Restaurant, User, UsersBadge, Badge, Rating, Favorite, Trip, Stop

import requests
from bs4 import BeautifulSoup as bs

def create_user(username, email, password, user_icon):

    user = User(
        username=username,
        email=email,
        password=password,
        user_icon=user_icon
    )
    
    return user

def get_user_by_email(email):

    user = User.query.filter_by(email=email).one()
    
    return user


def create_badge(badge_name, badge_icon, badge_description):
    """Create and return a new rating"""

    badge = Badge(
        badge_name = badge_name,
        badge_icon = badge_icon,
        badge_description = badge_description
    )

    return badge


def add_badge(user, badge):
    user.badges.append(badge)


def create_rating(thumbs_up, rating_icon, user_id, restaurant_id):

    rating = Rating(
        thumbs_up = thumbs_up,
        rating_icon = rating_icon,
        user_id = user_id,
        restaurant_id = restaurant_id
        )

    return rating


def create_trip(trip_name, trip_description, user_id):
     
     trip = Trip(
          trip_name = trip_name,
          trip_description = trip_description,
          user_id = user_id)
     
     return trip


def create_restaurant(restaurant_name, restaurant_icon, restaurant_description,
        restaurant_address, restaurant_state, food_type, episode_info):
        
        restaurant = Restaurant(
            restaurant_name = restaurant_name,
            restaurant_icon = restaurant_icon,
            restaurant_description = restaurant_description,
            restaurant_address = restaurant_address,
            restaurant_state = restaurant_state,
            food_type = food_type,
            episode_info = episode_info
            )
        
        return restaurant

def get_restaurants():
    """Return all restaurants"""

    return Restaurant.query.all()

def get_restaurants_by_id(restaurant_ids):
    """Return Restaurant object by restaurant_id"""

    restaurants = []

    for restaurant in restaurant_ids:
        restaurant = Restaurant.query.filter_by(restaurant_id=int(restaurant)).one()
        restaurants.append(restaurant)

    return restaurants

def is_user(email, password):
    """Return True/False if user/password combo in userDB. Confirms username and
        password are correct for login"""

    users = User.query.all()
    loggedIn = False

    for user in users:
        if email == user.email:
            if user.password == password:
                loggedIn = True

    return loggedIn

def email_exists(email):
    """Return True/False if username in userDB. Checking that same username 
        isn't creating multiple accounts"""

    users = User.query.all()
    exists = False

    for user in users:
        if email == user.email:
            exists = True

    return exists

def get_users():
    """Show all users, only used during development"""

    users = User.query.all()

    return users

def get_favorites(email):
    """Get all of a specific user's favorite restaurants"""

    user = get_user_by_email(email)

    favorites = user.restaurants

    return favorites

def add_favorites(email, favorites):
    """Add checked restaurants to user's favorites"""

    user = get_user_by_email(email)

    for favorite in favorites:
        if favorite not in user.restaurants:
            user.restaurants.append(favorite)

    # Do I need commits at any points like this because of the append?

def remove_favorites(email, remove_favorites):
    """Remove checked restaurants from user's favorites"""

    user = get_user_by_email(email)

    for restaurant in remove_favorites:
        removeobj = Favorite.query.filter_by(user_id=user.user_id, restaurant_id=int(restaurant)).one()

        db.session.delete(removeobj)

    db.session.commit()

def get_trips(email):
    user = get_user_by_email(email)

    trips = user.trips

    return trips

def get_trip_by_id(trip_id):
    trip = Trip.query.filter_by(trip_id=int(trip_id))

    return trip


def add_stops(trip_id, stops):
    """Add checked restaurants to user's trip"""

    trip = get_trip_by_id(trip_id)

    for stop in stops:
        if stop not in trip.restaurants:
            trip.restaurants.append(stop)

def add_trip_to_db(trip):
    db.session.add(trip)
    db.session.commit()

def remove_trips(email, remove_trips):
    """Remove checked restaurants from user's favorites"""

    user = get_user_by_email(email)

    for trip in remove_trips:
        removeobj = Trip.query.filter_by(user_id=user.user_id, trip_id=int(trip)).one()

        db.session.delete(removeobj)

    db.session.commit()

def get_stops(trips):
    for trip in trips:
        stops = Stop.query.filter_by(trip_id=trip.trip_id).all()

    return stops

def get_stop_restaurants(stops):

    restaurants_in_stops = []

    for stop in stops:
        restaurant = Restaurant.query.filter_by(restaurant_id=stop.restaurant_id).one()
        restaurants_in_stops.append(restaurant)

    return restaurants_in_stops

if __name__ == '__main__':
    from server import app
    connect_to_db(app)