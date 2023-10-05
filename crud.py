from model import User, UsersBadge, Badge, Rating, Trip, Restaurant
from model import db, connect_to_db


def create_user(username, email, password, user_icon):

    user = User(
        username=username,
        email=email,
        password=password,
        user_icon=user_icon
    )
    
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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)