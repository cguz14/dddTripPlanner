"""Server for movie ratings app."""

from flask import Flask

from pprint import pformat, pprint
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ['SECRETKEY']




# Replace this with routes and view functions!


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)