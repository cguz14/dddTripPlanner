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

# Can be executed with read_badges() as a parameter to add .txt badges to db
def update_badges():
    """Take dictionary of badges from txt and store in db"""

    existing_badges = Badge.query.all()

    print(existing_badges)
    # badges_to_add = []

    # for badge_name, badge_info in badges.items():
    #     (badge_icon, badge_description) = badge_info
    #     badge = create_badge(badge_name, badge_icon, badge_description)
        
    #     badges_to_add.append(badge)

