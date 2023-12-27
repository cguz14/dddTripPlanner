from model import connect_to_db, db, Restaurant, User, UsersBadge, Badge, Rating, Favorite, Trip, Stop

import requests
import os
import pprint
import time

from bs4 import BeautifulSoup as bs

def create_user(username, email, password, user_icon):

	user = User(
		username=username,
		email=email,
		password=password,
		user_icon=user_icon
	)
	
	return user


def get_user_by_email(email):

	user = User.query.filter_by(email=email).first()
	
	return user


def create_badge(badge_name, badge_icon, badge_description):
	"""Create and return a new badge"""

	badge = Badge(
		badge_name = badge_name,
		badge_icon = badge_icon,
		badge_description = badge_description
	)

	return badge


def add_badge(user, badge):
	user.badges.append(badge)


def create_rating(thumbs_up, rating_icon, user_id, restaurant_id):

	rating = Rating(
		thumbs_up = thumbs_up,
		rating_icon = rating_icon,
		user_id = user_id,
		restaurant_id = restaurant_id
		)

	return rating


def create_trip(trip_name, trip_description, user_id):
	 
	trip = Trip(
		trip_name = trip_name,
		trip_description = trip_description,
		user_id = user_id)
	
	return trip


def create_restaurant(restaurant_name, restaurant_icon, restaurant_description, restaurant_address,
											restaurant_latitude, restaurant_longitude, restaurant_state, food_type, episode_info):
		
	restaurant = Restaurant(
		restaurant_name = restaurant_name,
		restaurant_icon = restaurant_icon,
		restaurant_description = restaurant_description,
		restaurant_address = restaurant_address,
		restaurant_latitude = restaurant_latitude,
		restaurant_longitude = restaurant_longitude,
		restaurant_state = restaurant_state,
		food_type = food_type,
		episode_info = episode_info
		)
	
	return restaurant


def get_restaurants():
	"""Return all restaurants"""

	return Restaurant.query.all()


def get_restaurants_by_id(restaurant_ids):
	"""Return Restaurants list by restaurant_ids"""

	restaurants = []

	for restaurant in restaurant_ids:
		restaurant = Restaurant.query.filter_by(restaurant_id=int(restaurant)).one()
		restaurants.append(restaurant)

	return restaurants


def get_one_restaurant_by_id(restaurant_id):
	"""Return Restaurant object by restaurant_id"""

	return Restaurant.query.filter_by(restaurant_id=restaurant_id).one()


def is_user(email, password, check_password_hash):
	"""Return True/False if user/password combo in userDB. Confirms username and
	password are correct for login"""

	users = User.query.all()
	loggedIn = False

	for user in users:
		if email == user.email:
			if check_password_hash(user.password, password):
				loggedIn = True

	return loggedIn


def email_exists(email):
	"""Return True/False if email in userDB. Checking that same email 
	isn't creating multiple accounts"""

	users = User.query.all()
	exists = False

	for user in users:
		if email == user.email:
			exists = True

	return exists


def get_users():
	"""Show all users, only used during development"""

	users = User.query.all()

	return users


def get_favorites(email):
	"""Get all of a specific user's favorite restaurants"""

	user = get_user_by_email(email)

	favorites = user.restaurants

	return favorites


def add_favorites(email, favorites):
	"""Add checked restaurants to user's favorites"""

	user = get_user_by_email(email)

	for favorite in favorites:
		if favorite not in user.restaurants:
			user.restaurants.append(favorite)

	# Do I need commits at any points like this because of the append?
	db.session.commit()


def remove_favorites(email, remove_favorites):
	"""Remove checked restaurants from user's favorites"""

	user = get_user_by_email(email)

	for restaurant in remove_favorites:
		remove_obj = Favorite.query.filter_by(user_id=user.user_id, restaurant_id=int(restaurant)).one()

		db.session.delete(remove_obj)

	db.session.commit()


def get_trips(email):
	user = get_user_by_email(email)

	trips = user.trips

	return trips


def get_trip_by_id(trip_id):
	trip = Trip.query.filter_by(trip_id=trip_id).one()

	return trip


def add_stops(restaurants, trip_id):
	"""Add checked restaurants to user's trip"""

	trip = get_trip_by_id(trip_id)

	for restaurant in restaurants:
		if restaurant not in trip.restaurants:
			trip.restaurants.append(restaurant)

	db.session.commit()


def add_trip_to_db(trip):
	"""Add a given trip to the db"""
	
	db.session.add(trip)
	db.session.commit()


def remove_trips(remove_trip_id):
	"""Delete Selected trip from db"""

	remove_obj = Trip.query.filter_by(trip_id=remove_trip_id).one()

	db.session.delete(remove_obj)
	db.session.commit()


def get_stops(trips):
	
	for trip in trips:
		stops = Stop.query.filter_by(trip_id=trip.trip_id).all()

	return stops


def get_stop_restaurants(stops):

	restaurants_in_stops = []

	for stop in stops:
		restaurant = Restaurant.query.filter_by(restaurant_id=stop.restaurant_id).one()
		restaurants_in_stops.append(restaurant)

	return restaurants_in_stops


def remove_stops(restaurant_ids, trip_id):

	for restaurant_id in restaurant_ids:
		remove_obj = Stop.query.filter_by(restaurant_id=restaurant_id, trip_id=trip_id).one()

		db.session.delete(remove_obj)

	db.session.commit()


def convert_address_to_geocode(address):

	GEO_PLACES_KEY = os.environ['GEO_PLACES_KEY']

	# address = address.split()

	param_address = ""

	for char in address:
		if char == "#":
			encoded_char = f"%23"            
			param_address += encoded_char
		elif char == "/":
			encoded_char = f"%2F"            
			param_address += encoded_char
		elif char == " ":
			encoded_char = f"%20"
			param_address += encoded_char
		else:
			param_address += char

	url = f"https://maps.googleapis.com/maps/api/geocode/json?address={param_address}&key={GEO_PLACES_KEY}"

	response = requests.get(url)
	# Ugly way to retrieve specific value needed from json dict. Any other recommendations
	print(response.json()['status'])

	if response.json()['status'] == 'INVALID_REQUEST':
		return response.json()['status']
	elif response.json()['status'] == 'ZERO_RESULTS':
		return response.json()['status']

	address_geocoded = response.json().get('results')[0]

	return address_geocoded


def get_latitude(address_geocoded):

	return address_geocoded['geometry']['location']['lat']


def get_longitude(address_geocoded):

	return address_geocoded['geometry']['location']['lng']


def get_formatted_address(address_geocoded):

	address_info = address_geocoded['address_components']
	location_type = address_geocoded['geometry']['location_type']

	for info in address_info:
		if "country" in info['types']:
			country = info['long_name']

	if country != 'United States':
		return None
	elif location_type == "APPROXIMATE":
		return "(Approximate Location) " + address_geocoded['formatted_address']

	return address_geocoded['formatted_address']


def get_city_and_state(address_geocoded):
	
	address_info = address_geocoded['address_components']

	print(address_geocoded)

	state = ''
	city = ''

	for info in address_info:
		if "administrative_area_level_1" in info['types']:
			state = info['short_name']
		elif "locality" in info['types']:
			city = info['long_name']
		elif "country" in info['types']:
			country = info['long_name']
		elif "postal_town" in info['types']:
			city = info['long_name']

	if city == '':
		return country

	if country != "United States":
		city_and_state = city + ", " + country
	else:
		city_and_state = city + ", " + state

	return city_and_state


def get_place_id(address_geocoded):

	return address_geocoded['place_id']


def change_like(liked, user, restaurant_id):
	
	if rating_exists(user, restaurant_id):
		rating = Rating.query.filter_by(user_id = user.user_id, restaurant_id = restaurant_id).one()
		old_rate = rating.thumbs_up
		remove_rating(user, restaurant_id)
		# This runs if there is a change in the rating from up to down or vice-versa
		if old_rate != liked:
			add_rating(liked, user, restaurant_id)
	else:
		add_rating(liked, user, restaurant_id)


def add_rating(liked, user, restaurant_id):
	new_rating = create_rating(liked, "imgNotBeingUsed", user.user_id, restaurant_id)

	db.session.add(new_rating)
	db.session.commit()


def remove_rating(user, restaurant_id):

	rating = Rating.query.filter_by(user_id = user.user_id, restaurant_id = restaurant_id).one()

	db.session.delete(rating)
	db.session.commit()


def rating_exists(user, restaurant_id):

	rating = Rating.query.filter_by(user_id = user.user_id, restaurant_id = restaurant_id).first()

	if rating:
		return True
	
	return False


def get_ratings(user):

	return user.ratings


def get_rating_restaurant_ids(ratings):

	restaurant_ids = []

	for rating in ratings:
		restaurant_ids.append(rating.restaurant_id)

	return restaurant_ids


def award_badge(email, badge_id):
	"""Add badge to user account"""
	
	if not check_for_badge(email, badge_id):
		user = get_user_by_email(email)
		award_badge = Badge.query.filter_by(badge_id = badge_id).one()

		user.badges.append(award_badge)
		db.session.commit()

		return award_badge
	
	else:
		print('Error in award_badge() call, user already has badge for id being awarded')
		return None


def get_all_badges():

	badges = {}

	for user in User.query.all():
		badges[user]=user.badges

	return badges


def check_for_badge(email, badge_id):

	user_badges = get_user_by_email(email).badges

	if user_badges:
		for badge in user_badges:
			if badge.badge_id == badge_id:
				return True
		
	return False


def make_maps_param(start_address, end, ordered_stops):

	stops = []

	ordered_list = ordered_stops.split('QQQQQ')

	# Used when there are no in between stops and only one destination
	if start_address and end and ordered_list == ['','']:
		stops.append({
			"restaurant_id" : "User Address Start Point",
			"restaurant_name" : "User Address Start Point",
			"restaurant_icon" : "User Address Start Point",
			"restaurant_description" : "User Address Start Point",
			"restaurant_address" : start_address,
			"restaurant_latitude" :"User Address Start Point",
			"restaurant_longitude" : "User Address Start Point",
			"restaurant_state" : "User Address Start Point",
			"food_type" : "User Address Start Point",
			"episode_info" : "User Address Start Point"
		})

		# place selected end point as last address in list
		stops.append({
			"restaurant_id" : end.restaurant_id,
			"restaurant_name" : end.restaurant_name,
			"restaurant_icon" : end.restaurant_icon,
			"restaurant_description" : end.restaurant_description,
			"restaurant_address" : end.restaurant_address,
			"restaurant_latitude" : end.restaurant_latitude,
			"restaurant_longitude" : end.restaurant_longitude,
			"restaurant_state" : end.restaurant_state,
			"food_type" : end.food_type,
			"episode_info" : end.episode_info
		})

		# since start address was entered, origin param needed        
		param_address = "origin="

		for idx, stop in enumerate(stops):
			address = stop['restaurant_address'].lstrip()

			if idx == 1:
				param_address += "&destination="

			for char in address:
				if char == "#":
					encoded_char = f"%23"            
					param_address += encoded_char
				elif char == "/":
					encoded_char = f"%2F"            
					param_address += encoded_char
				elif char.strip() == '':
					encoded_char = f"%20"
					param_address += encoded_char
				elif char == ",":
					encoded_char = f"%2C"
					param_address += encoded_char
				elif char == ".":
					encoded_char = f"%2E"
					param_address += encoded_char
				elif char == '"':
					encoded_char = f"%22"
					param_address += encoded_char
				else:
					param_address += char

	else:
		# Used when there are multiple waypoints
		if start_address and end:

			stops.append({
				"restaurant_id" : "User Address Start Point",
				"restaurant_name" : "User Address Start Point",
				"restaurant_icon" : "User Address Start Point",
				"restaurant_description" : "User Address Start Point",
				"restaurant_address" : start_address,
				"restaurant_latitude" :"User Address Start Point",
				"restaurant_longitude" : "User Address Start Point",
				"restaurant_state" : "User Address Start Point",
				"food_type" : "User Address Start Point",
				"episode_info" : "User Address Start Point"
			})

			# Get ordered_stop addresses added to Maps URL Parameter in 
			# optimized order given by Directions API
			for ordered_stop in ordered_list:
				if ordered_stop != end.restaurant_address:
					stops.append({
						"restaurant_id" : "ordered stop",
						"restaurant_name" : "ordered stop",
						"restaurant_icon" : "ordered stop",
						"restaurant_description" : "ordered stop",
						"restaurant_address" : ordered_stop,
						"restaurant_latitude" : "ordered stop",
						"restaurant_longitude" : "ordered stop",
						"restaurant_state" : "ordered stop",
						"food_type" : "ordered stop",
						"episode_info" : "ordered stop"
					})

			# place selected end point as last address in list
			stops.append({
				"restaurant_id" : end.restaurant_id,
				"restaurant_name" : end.restaurant_name,
				"restaurant_icon" : end.restaurant_icon,
				"restaurant_description" : end.restaurant_description,
				"restaurant_address" : end.restaurant_address,
				"restaurant_latitude" : end.restaurant_latitude,
				"restaurant_longitude" : end.restaurant_longitude,
				"restaurant_state" : end.restaurant_state,
				"food_type" : end.food_type,
				"episode_info" : end.episode_info
			})

			# since start address was entered, origin param needed        
			param_address = "origin="

			for idx, stop in enumerate(stops):
				address = stop['restaurant_address'].lstrip()

				if idx == 1:
					param_address += "&waypoints="

				if idx == len(stops)-1:
					param_address += "&destination="

				for char in address:
					if char == "#":
						encoded_char = f"%23"            
						param_address += encoded_char
					elif char == "/":
						encoded_char = f"%2F"            
						param_address += encoded_char
					elif char.strip() == '':
						encoded_char = f"%20"
						param_address += encoded_char
					elif char == ",":
						encoded_char = f"%2C"
						param_address += encoded_char
					elif char == ".":
						encoded_char = f"%2E"
						param_address += encoded_char
					elif char == '"':
						encoded_char = f"%22"
						param_address += encoded_char
					else:
						param_address += char

				if idx > 0 and idx < len(stops)-2:
					param_address += f"%7C"

	return param_address


def get_states_restaurants(state):

	filtered_restaurants = Restaurant.query.filter(Restaurant.restaurant_state.endswith(state)).all()

	return filtered_restaurants


def get_restaurant_state_dict():

	state_list = [
		'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
		'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
		'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
		'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
		'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
	]
	full_state_list = [
		'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
		'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
		'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
		'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
		'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
		'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
		'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 
		'Wisconsin', 'Wyoming'
	]
	restaurant_state_dict = {}

	for idx, state in enumerate(state_list):
		# restaurant_state currently returns full 'City, ST'
		restaurant_state_dict[state] = {}
		filtered_restaurants = get_states_restaurants(state)
		restaurant_state_dict[state][full_state_list[idx]] = filtered_restaurants

	return restaurant_state_dict


if __name__ == '__main__':
	from server import app
	connect_to_db(app)