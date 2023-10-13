"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
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
app.jinja_env.undefined = StrictUndefined

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

@app.route('/login', methods=["POST"])
def user_login():
    """User Profile Page"""

    email = request.form.get("email")
    password = request.form.get("password")
    # need way to query user_id, username, and icon from User db using email
    user = crud.get_user_by_email(email)

    # if "email" in session:
    #     flash(f"You're already logged in {session['email']}")
    #     return redirect("/")
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
        # user = crud.get_user(session["user_id"])
        return render_template("profile.html")
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
    else:
        user = crud.create_user(username, email, password, user_icon)
        db.session.add(user)
        db.session.commit()
        session["username"] = username
        session["email"] = email
        session["user_id"] = user.user_id
        session["user_icon"] = user_icon
        flash("You're on your way to FlavorTown!")

        return redirect('/profile')
   
@app.route('/new-account')
def create_account_page():
    
    # if "email" in session:
    #     flash(f"You're already logged in! {session['email']}")
    #     return redirect("/")
    
    return render_template('new_account.html')

@app.route('/all-users')
def all_users():

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route('/favorites')
def favorites():

    if "email" in session:
        favorites = crud.get_favorites(session["email"])
        return render_template('favorites.html', favorites=favorites)
    else:
        flash("You need to login first!")
        return redirect("/")

# @app.route('/restaurants')
# def show_real_restaurants():

#     soup = crud.get_real_restaurants()

#     return render_template('restaurants.html', soup=soup)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)