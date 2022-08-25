from datetime import datetime

from flask import session

from ..utils.authentication import get_current_user_id
from ..models.user import User


def check_user_in_database() -> bool:
    user_id = get_current_user_id(session)
    user_query = User.query.filter_by(auth0_id=user_id).one_or_none()
    return user_query is not None


def register_user() -> None:
    auth0_id = get_current_user_id(session)
    username = session["user"]["userinfo"]["name"]
    email = session["user"]["userinfo"]["email"]
    updated_at = session["user"]["userinfo"]["updated_at"]

    new_user = User(auth0_id, username, email, updated_at)
    new_user.insert()


def user_info_needs_updating() -> bool:
    user_id = get_current_user_id(session)
    updated_at_str = session["user"]["userinfo"]["updated_at"]
    updated_at = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    user = User.query.filter_by(auth0_id=user_id).one()
    return updated_at != user.updated_at


def update_user() -> None:
    user_id = get_current_user_id(session)
    user = User.query.filter_by(auth0_id=user_id).one()

    user.username = session["user"]["userinfo"]["name"]
    user.email = session["user"]["userinfo"]["email"]
    user.updated_at = session["user"]["userinfo"]["updated_at"]
    user.update()
