"""Server for movie ratings app."""

from flask import Flask, render_template, request

from pprint import pformat, pprint
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRETKEY']

app.config['ORESERVE_CONTEXT_ON_EXCEPTION'] = True

# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """Show homepage"""

    return render_template('homepage.html')


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)