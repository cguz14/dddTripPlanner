"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

from flask import Flask, request
from bs4 import BeautifulSoup as bs

import crud
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

n=0
while n < 10:
    new_user = crud.create_user(username=f"billyDags{n}",
                                email=f"billy{n}@dags.com",
                                password=f"password{n}",                                
                                user_icon="dddTripPlanner/imgs/guyFaceCredKRSheehan.png")
    users_in_db.append(new_user)
    
    n += 1

model.db.session.add_all(users_in_db)
model.db.session.commit()

n=0
while n < 10:
    new_badge = crud.create_badge(f"testBadge{n}",
                                  "dddTripPlanner/imgs/10PlusIcon.png",
                                  f"testdescription{n}")
    badges_in_db.append(new_badge)

    n += 1

model.db.session.add_all(badges_in_db)
model.db.session.commit()

n=0
while n < 5:

    users_in_db[n].badges.append(badges_in_db[n+3])

    n += 1

model.db.session.commit()


n=0
while n < 1:

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
        restaurant_state = crud.get_state(address_geocoded)
        place_id =  crud.get_place_id(address_geocoded)
        # episode_info = info pull from wiki web scrape?

        if restaurant.find(class_="m-MediaBlock__a-Image"):
            img = restaurant.find(class_="m-MediaBlock__a-Image").get("src")
        else:
            img = "static/img/attachment-guys-diner-background.jpg"

        new_restaurant = crud.create_restaurant(
            name,
            img,
            description,
            formatted_address,
            restaurant_latitude,
            restaurant_longitude,
            restaurant_state,
            place_id, # need to ensure change is reflected in rest of program. No longer food_type. Place Id can be used to pull more information from Places API
            f"test_episode_info{n}"
        )

        print(name)
        print(formatted_address)
        print(restaurant_state)
        print(place_id)
        print("*********************")

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

print(restaurants_in_db)
model.db.session.add_all(restaurants_in_db)
model.db.session.commit()


n=0
while n < 10:


    new_rating = crud.create_rating((n%2 == 0),
                                    "imgs/thumbs-up-line-icon.svg",
                                    users_in_db[n].user_id,
                                    restaurants_in_db[9-n].restaurant_id)

    ratings_in_db.append(new_rating)
    
    n += 1

model.db.session.add_all(ratings_in_db)
model.db.session.commit()

n=0
while n < 5:

    users_in_db[n].restaurants.append(restaurants_in_db[n*2])

    n += 1

model.db.session.commit()


n=0
while n < 5:

    new_trip = crud.create_trip(f"testTrip{n}",
                                f"testDescription{n}",
                                users_in_db[9-(n*2)].user_id)

    trips_in_db.append(new_trip)

    n += 1

model.db.session.add_all(trips_in_db)
model.db.session.commit()


n=0
while n < 5:

    trips_in_db[(int(n/2))].restaurants.append(restaurants_in_db[(9-n)])

    n += 1




model.db.session.commit()