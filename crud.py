from model import db, User, UsersBadge, Badge, connect_to_db


def create_user(username,email,password, user_icon):

    user = User(
        username=username,
        email=email,
        password=password,
        user_icon=user_icon
    )
    
    return user

# So do I not need a crud for the middle table then?
# def create_users_badge(user, badge):
#     """Create and return a new movie."""

#     users_badge = UsersBadge(user=user, badge=badge)

#     return users_badge


def create_badge(badge_name, badge_icon, badge_description):
    """Create and return a new rating"""

    badge = Badge(
        badge_name=badge_name,
        badge_icon=badge_icon,
        badge_description=badge_description
    )

    return badge


if __name__ == '__main__':
    from server import app
    connect_to_db(app)