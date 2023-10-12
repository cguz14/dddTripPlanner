"""Server for movie ratings app."""

from flask import Flask, render_template, request
import crud
from model import connect_to_db, Restaurant, User, UsersBadge, Badge, Rating, Favorite, Trip, Stop
from pprint import pformat, pprint
from bs4 import BeautifulSoup as bs
import os
import json
import requests

app = Flask(__name__)
app.secret_key = os.environ['SECRETKEY']

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

# @app.route('/restaurants')
# def show_real_restaurants():

#     soup = crud.get_real_restaurants()

#     return render_template('restaurants.html', soup=soup)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)