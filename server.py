"""Server for movie ratings app."""

from flask import Flask, render_template, request
import crud

from pprint import pformat, pprint
import os

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


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)