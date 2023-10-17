"""Models for DDD Trip Planner app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!
class User(db.Model): #User
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    user_icon = db.Column(db.String(100))
    
    trips = db.relationship("Trip", back_populates = "user")
    ratings = db.relationship("Rating", back_populates = "user")
    
    badges = db.relationship("Badge",
                             secondary="usersbadges",
                             back_populates = "users")
    restaurants = db.relationship("Restaurant",
                                  secondary = "favorites",
                                  back_populates = "users")

    def __repr__(self):
        return f'<User username={self.username} email={self.email}>'

class UsersBadge(db.Model): 
    """A User's Unlocked Badge's"""

    __tablename__= "usersbadges"
    
    users_badge_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    unlocked_badge_id = db.Column(db.Integer, db.ForeignKey("badges.badge_id"))

    def __repr__(self):
        return f'<Badges user_id={self.user_id} badges_id={self.users_badge_id}>'

class Badge(db.Model):
    """A badge"""

    __tablename__ = "badges"

    badge_id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    badge_name = db.Column(db.String(50))
    badge_icon = db.Column(db.String(100))
    badge_description = db.Column(db.Text)
    
    users = db.relationship("User",
                            secondary="usersbadges",
                            back_populates="badges")
    
    def __repr__(self):
        return f'<Badge badge_id={self.badge_id} desc={self.badge_description}>'
    

class Rating(db.Model):
    """A rating"""

    __tablename__ = "ratings"

    rating_id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    thumbs_up = db.Column(db.Boolean)
    rating_icon = db.Column(db.String(100))
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"))

    user = db.relationship("User", back_populates = "ratings")
    restaurant = db.relationship("Restaurant", back_populates = "ratings")

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} user={self.user_id} thumbUp={self.thumbs_up}>'
    

class Restaurant(db.Model):
    """A restaurant"""

    __tablename__ = "restaurants"

    restaurant_id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    restaurant_name = db.Column(db.String(100))
    restaurant_icon = db.Column(db.Text, nullable = True)
    restaurant_description = db.Column(db.Text)
    restaurant_address = db.Column(db.String(250))
    restaurant_state = db.Column(db.String(25))
    food_type = db.Column(db.String(25))
    episode_info = db.Column(db.String(50))
    
    ratings = db.relationship("Rating", back_populates = "restaurant")
    
    users = db.relationship("User",
                            secondary = "favorites",
                            back_populates = "restaurants")
    trips = db.relationship("Trip",
                            secondary = "stops",
                            back_populates = "restaurants")

    def __repr__(self):
        return f'<Restaurant name={self.restaurant_name} desc={self.restaurant_description}>'


class Favorite(db.Model): 
    """A User's Restaurant Favorites"""

    __tablename__= "favorites"
    
    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"))

    def __repr__(self):
        return f'<Favorite user_id={self.user_id} restaurant_id={self.restaurant_id}>'
    

class Trip(db.Model):
    """A User's planned trip"""

    __tablename__= "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    trip_name = db.Column(db.String(50))
    trip_description = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", back_populates = "trips")

    restaurants = db.relationship("Restaurant",
                                  secondary = "stops",
                                  back_populates = "trips")

    def __repr__(self):
        return f'<Trip name={self.trip_name} desc={self.trip_description}>'
    
class Stop(db.Model):
    """A User's Unlocked Badge's"""

    __tablename__= "stops"
    
    stop_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"))

    def __repr__(self):
        return f'<Stop trip_id={self.trip_id} restaurant_id={self.restaurant_id}>'
    

def connect_to_db(flask_app, db_uri="postgresql:///dddTripPlanner", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    db.app = flask_app
    db.init_app(flask_app)

    print("We are in le Project model")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)