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
while n < 86:

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
        if restaurant.find(class_="m-MediaBlock__a-Image"):
            img = restaurant.find(class_="m-MediaBlock__a-Image").get("src")
        else:
            img = None

        new_restaurant = crud.create_restaurant(
            f"{name}",
            f"{img}",
            f"{description}",
            f"{address}",
            f"testrestaurant_state{n}",
            f"testfood_type{n}",
            f"testepisode_info{n}"
        )

        restaurants_in_db.append(new_restaurant)

    n += 1

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