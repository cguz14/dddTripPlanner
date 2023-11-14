from model import connect_to_db, db, Restaurant, User, UsersBadge, Badge, Rating, Favorite, Trip, Stop
from crud import create_badge

def read_badges():
	"""Reads in badge information from badges.txt file so badges can be updated over time"""
	"""Badge info is stored as a dictionary with the name as the key and a tuple of the
		badge icon and description as its value."""

	badges_txt = open('./static/txt/badges.txt')

	badges = {}

	for line in badges_txt:
		line = line.rstrip()
		badge_id, badge_name, badge_icon, badge_description = line.split(':')
		badge_info = (badge_name, badge_icon, badge_description)
		badges[badge_id] = badge_info

	return badges

# Can be executed with read_badges() as a parameter to add updated .txt badges to db
def update_badges(updated_badges):
	"""Take dictionary of badges from txt and store in db"""

	for badge_id, badge_info in updated_badges.items():
		badge_name, badge_icon, badge_description = badge_info
		existing_badge = Badge.query.filter_by(badge_id=badge_id).first()

		if existing_badge:
			if (existing_badge.badge_name != badge_name
			or existing_badge.badge_description != badge_description
			or existing_badge.badge_icon != badge_icon):
				existing_badge.badge_name = badge_name
				existing_badge.badge_description = badge_description
				existing_badge.badge_icon = badge_icon

				print(f'Badge_id: {badge_id} Updated')
		else:
			new_badge = create_badge(badge_name, badge_icon, badge_description)
			db.session.add(new_badge)
			print(f'Badge_id: {new_badge.badge_id} Created. Confirm that txt file badge id matches')
			print(new_badge.badge_name, new_badge.badge_icon, new_badge.badge_description)
			
		db.session.commit()

if __name__ == "__main__":
	from server import app

	connect_to_db(app)

update_badges(read_badges())