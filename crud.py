from model import connect_to_db, db, Restaurant, User, UsersBadge, Badge, Rating, Favorite, Trip, Stop

import requests
import os
import pprint
import time

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

    user = User.query.filter_by(email=email).first()
    
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
        restaurant_address, restaurant_latitude, restaurant_longitude, restaurant_state, food_type, episode_info):
        
        restaurant = Restaurant(
            restaurant_name = restaurant_name,
            restaurant_icon = restaurant_icon,
            restaurant_description = restaurant_description,
            restaurant_address = restaurant_address,
            restaurant_latitude = restaurant_latitude,
            restaurant_longitude = restaurant_longitude,
            restaurant_state = restaurant_state,
            food_type = food_type,
            episode_info = episode_info
            )
        
        return restaurant

def get_restaurants():
    """Return all restaurants"""

    return Restaurant.query.all()

def get_restaurants_by_id(restaurant_ids):
    """Return Restaurants list by restaurant_ids"""

    restaurants = []

    for restaurant in restaurant_ids:
        restaurant = Restaurant.query.filter_by(restaurant_id=int(restaurant)).one()
        restaurants.append(restaurant)

    return restaurants

def get_one_restaurant_by_id(restaurant_id):
    """Return Restaurant object by restaurant_id"""

    return Restaurant.query.filter_by(restaurant_id=restaurant_id).one()

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
    db.session.commit()

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
    trip = Trip.query.filter_by(trip_id=trip_id).one()

    return trip

def add_stops(restaurants, trip_id):
    """Add checked restaurants to user's trip"""

    trip = get_trip_by_id(trip_id)

    for restaurant in restaurants:
        if restaurant not in trip.restaurants:
            trip.restaurants.append(restaurant)

    db.session.commit()

def add_trip_to_db(trip):
    """Add a given trip to the db"""
    
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

def remove_stops(restaurant_ids, trip_id):

    for restaurant_id in restaurant_ids:
        removeobj = Stop.query.filter_by(restaurant_id=restaurant_id, trip_id=trip_id).one()

        db.session.delete(removeobj)

    db.session.commit()

def convert_address_to_geocode(address):

    MAPS_KEY = os.environ['MAPS_KEY']

    # address = address.split()

    param_address = ""

    for char in address:
        if char == "#":
            encoded_char = f"%23"            
            param_address += encoded_char
        elif char == "/":
            encoded_char = f"%2F"            
            param_address += encoded_char
        elif char == " ":
            encoded_char = f"%20"
            param_address += encoded_char
        else:
            param_address += char

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={param_address}&key={MAPS_KEY}"

    response = requests.get(url)
    # Ugly way to retrieve specific value needed from json dict. Any other recommendations
    address_geocoded = response.json().get('results')[0].get('geometry').get('location')

    return address_geocoded

def get_latitude(address_geocoded):

    return address_geocoded['lat']

def get_longitude(address_geocoded):

    return address_geocoded['lng']

def change_like(liked, user, restaurant_id):
    
    if rating_exists(user, restaurant_id):
        rating = Rating.query.filter_by(user_id = user.user_id, restaurant_id = restaurant_id).one()
        old_rate = rating.thumbs_up
        remove_rating(user, restaurant_id)
        # This runs if there is a change in the rating from up to down or vice-versa
        if old_rate != liked:
            add_rating(liked, user, restaurant_id)
    else:
        add_rating(liked, user, restaurant_id)

def add_rating(liked, user, restaurant_id):
    new_rating = create_rating(liked, "imgNotBeingUsed", user.user_id, restaurant_id)

    db.session.add(new_rating)
    db.session.commit()

def remove_rating(user, restaurant_id):

    rating = Rating.query.filter_by(user_id = user.user_id, restaurant_id = restaurant_id).one()

    db.session.delete(rating)
    db.session.commit()

def rating_exists(user, restaurant_id):

    rating = Rating.query.filter_by(user_id = user.user_id, restaurant_id = restaurant_id).first()

    if rating:
        return True
    
    return False

def get_ratings(user):

    return user.ratings

def get_rating_restaurant_ids(ratings):

    restaurant_ids = []

    for rating in ratings:
        restaurant_ids.append(rating.restaurant_id)

    return restaurant_ids

def read_badges():
    """Reads in badge information from badges.txt file so badges can be updated over time"""
    """Badge info is stored as a dictionary with the name as the key and a tuple of the
        badge icon and description as its value."""

    badges_txt = open('./static/txt/badges.txt')

    badges = {}

    for line in badges_txt:
        line = line.rstrip()
        badge_name, badge_icon, badge_description = line.split(':')
        badge_info = (badge_icon, badge_description)
        badges[badge_name] = badge_info

    return badges

def create_badges(badges):
    """Take dictionary of badges from txt and store in db"""

    badges_to_add = []

    for badge_name, badge_info in badges.items():
        (badge_icon, badge_description) = badge_info
        badge = create_badge(badge_name, badge_icon, badge_description)
        
        badges_to_add.append(badge)

    db.session.add_all(badges_to_add)
    db.session.commit()

def award_badge(email, badge_id):
    """Add badge to user account"""
    
    if not check_for_badge(email, badge_id):
        user = get_user_by_email(email)
        award_badge = Badge.query.filter_by(badge_id = badge_id).one()

        user.badges.append(award_badge)
        db.session.commit()

        return award_badge
    
    else:
        print('Error in award_badge() call, user already has badge for id being awarded')
        return None

def get_all_badges():

    badges = {}

    for user in User.query.all():
        badges[user]=user.badges

    return badges

def check_for_badge(email, badge_id):

    user_badges = get_user_by_email(email).badges

    if user_badges:
        for badge in user_badges:
            if badge.badge_id == badge_id:
                return True
        
    return False

# Used crud to update badges after badges were created, run file interactively
# def update_badges_DEV_ONLY():
#     users = User.query.all()
#     # badge = Badge.query.filter_by(badge_id = 13).one()

#     for user in users:

#         if not check_for_badge(user.email, 13):
#             awarded_badge = award_badge(user.email, 13)
#             print(f'{awarded_badge.badge_name} awarded to {user}')
            
#     print('badges updated')

if __name__ == '__main__':
    from server import app
    connect_to_db(app)