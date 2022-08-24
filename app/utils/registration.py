from datetime import datetime

from flask import session

from ..models.user import User

CURRENT_USER_ID = session["user"]["userinfo"]["sub"].split("|")[-1]


def check_user_in_database() -> bool:
    user_query = User.query.filter_by(auth0_id=CURRENT_USER_ID).one_or_none()
    return user_query is not None


def register_user() -> None:
    username = session["user"]["userinfo"]["name"]
    email = session["user"]["userinfo"]["email"]
    updated_at = session["user"]["userinfo"]["updated_at"]

    new_user = User(CURRENT_USER_ID, username, email, updated_at)
    new_user.insert()


def user_info_needs_updating() -> bool:
    updated_at_str = session["user"]["userinfo"]["updated_at"]
    updated_at = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    user = User.query.filter_by(auth0_id=CURRENT_USER_ID).one()
    return updated_at == user.updated_at


def update_user() -> None:
    user = User.query.filter_by(auth0_id=CURRENT_USER_ID).one()

    user.username = session["user"]["userinfo"]["name"]
    user.email = session["user"]["userinfo"]["email"]
    user.updated_at = session["user"]["userinfo"]["updated_at"]
    user.update()
