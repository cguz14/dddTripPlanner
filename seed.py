"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb dddTripPlanner")
os.system("createdb dddTripPlanner")

model.connect_to_db(server.app)
model.db.create_all()

users_in_db = []
badges_in_db =[]
users_badge_in_db = []

n=0
while n < 10:
    new_user = crud.create_user(f"billyDags{n}",
                                f"password{n}",
                                f"billy{n}@dags.com",
                                "dddTripPlanner/imgs/guyFaceCredKRSheehan.png")
    users_in_db.append(new_user)
    
    n += 1

model.db.session.add_all(users_in_db)

n=0
while n < 10:
    new_badge = crud.create_badge(f"testBadge{n}",
                                  "dddTripPlanner/imgs/10PlusIcon.png",
                                  f"testdescription{n}")
    badges_in_db.append(new_badge)

    n += 1

model.db.session.add_all(badges_in_db)

n=0
while n < 5:

    users_in_db[n].badges.append(badges_in_db[n+3])

    n += 1

model.db.session.commit()