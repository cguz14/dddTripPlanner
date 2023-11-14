"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

from flask import Flask, request
from bs4 import BeautifulSoup as bs

import crud
import update_badges
import model
import server
import requests
import time

os.system("dropdb dddTripPlanner")
os.system("createdb dddTripPlanner")

model.connect_to_db(server.app)
model.db.create_all()

users_in_db = []
badges_in_db = []
users_badge_in_db = []
restaurants_in_db = []
ratings_in_db = []
trips_in_db = []

# **** Seeds test users if desired
# n=0
# while n < 10:
#     new_user = crud.create_user(username=f"billyDags{n}",
#                                 email=f"billy{n}@dags.com",
#                                 password=f"password{n}",                                
#                                 user_icon="dddTripPlanner/imgs/guyFaceCredKRSheehan.png")
#     users_in_db.append(new_user)
    
#     n += 1

# model.db.session.add_all(users_in_db)
# model.db.session.commit()

# **** Seeds test badges, unnecessary once custom badges are introduced
# n=0
# while n < 10:
#     new_badge = crud.create_badge(f"testBadge{n}",
#                                   "dddTripPlanner/imgs/10PlusIcon.png",
#                                   f"testdescription{n}")
#     badges_in_db.append(new_badge)

#     n += 1

# model.db.session.add_all(badges_in_db)
# model.db.session.commit()

# **** Seeds test badges awarded to test users. Not needed if reading badges in
# n=0
# while n < 5:

#     users_in_db[n].badges.append(badges_in_db[n+3])

#     n += 1

# model.db.session.commit()


n=0
while n < 0: # set to 0 while not seeding to avoid reusing key. needs to be 86 when seeding

    url = f"https://www.foodnetwork.com/restaurants/shows/diners-drive-ins-and-dives/a-z/p/{n+1}"

    response = requests.get(url)
    time.sleep(0.5)
    html = response.content
    soup = bs(html, 'html.parser')

    restaurants = []

    restaurants = soup.select("section.o-ListPointOfInterest div.m-MediaBlock")

    print(f"Page: {n+1}")

    for restaurant in restaurants:
        name = restaurant.find(class_="m-MediaBlock__a-HeadlineText").get_text()
        address = restaurant.find(class_="m-Info__a-Address").get_text()
        description = restaurant.find(class_="m-MediaBlock__a-Description").get_text()
        address_geocoded = crud.convert_address_to_geocode(address) # this is also able to pull api information
        restaurant_latitude = crud.get_latitude(address_geocoded)
        restaurant_longitude = crud.get_longitude(address_geocoded)
        formatted_address = crud.get_formatted_address(address_geocoded)
        if not formatted_address: # Checks if address is in USA, if not, then keeps address as scraped. Issue caught with Cuban addresses.
            formatted_address = address.strip()
        restaurant_state = crud.get_city_and_state(address_geocoded)
        place_id =  crud.get_place_id(address_geocoded)
        # episode_info = info pull from wiki web scrape?

        if restaurant.find(class_="m-MediaBlock__a-Image"):
            img = restaurant.find(class_="m-MediaBlock__a-Image").get("src")
        else:
            img = "static/img/attachment-guys-diner-background.jpg"

        new_restaurant = crud.create_restaurant(
            name.strip(),
            img.strip(),
            description.strip(),
            formatted_address.strip(),
            restaurant_latitude,
            restaurant_longitude,
            restaurant_state.strip(),
            place_id.strip(), # need to ensure change is reflected in rest of program. No longer food_type. Place Id can be used to pull more information from Places API
            f"test_episode_info{n}"
        )

        can_add=True
        old_address = ""
        if len(restaurants_in_db)>1:
            for restaurant in restaurants_in_db:
                old_address = restaurant.restaurant_address
                if old_address == new_restaurant.restaurant_address:
                    can_add=False

        if can_add:
            restaurants_in_db.append(new_restaurant)

    n += 1

model.db.session.add_all(restaurants_in_db)
model.db.session.commit()

# Seeds badges by reading info from badges.txt file. Run update_badges.py anytime more updates are made.
# Ensure badge_ids align in the awarded locations throughout the server.py file
update_badges.update_badges(update_badges.read_badges())

# ****Rating seed not needed unless wanting test ratings
# n=0
# while n < 10:

#     new_rating = crud.create_rating((n%2 == 0),
#                                     "imgs/thumbs-up-line-icon.svg",
#                                     users_in_db[n].user_id,
#                                     restaurants_in_db[9-n].restaurant_id)

#     ratings_in_db.append(new_rating)
    
#     n += 1

# model.db.session.add_all(ratings_in_db)
# model.db.session.commit()

# ****This will seed user favorited restaurants as part of seed if test favorites are desired
# n=0
# while n < 5:

#     users_in_db[n].restaurants.append(restaurants_in_db[n*2])

#     n += 1

# model.db.session.commit()

# ****Adds trips for seed if test trips are desired
# n=0
# while n < 5:

#     new_trip = crud.create_trip(f"testTrip{n}",
#                                 f"testDescription{n}",
#                                 users_in_db[9-(n*2)].user_id)

#     trips_in_db.append(new_trip)

#     n += 1

# model.db.session.add_all(trips_in_db)
# model.db.session.commit()

# ****Adds stops to test trips for seed if desired
# n=0
# while n < 5:

#     trips_in_db[(int(n/2))].restaurants.append(restaurants_in_db[(9-n)])

#     n += 1


model.db.session.commit()