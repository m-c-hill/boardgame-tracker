from os import environ as env
from urllib.parse import quote_plus, urlencode

from flask import jsonify, redirect, session, url_for

from app import oauth
from app.utils.authentication import get_current_user_id

from ..utils.registration import (
    check_user_in_database,
    register_user,
    update_user,
    user_info_needs_updating,
)
from . import auth


# Dummy endpoint for development purposes to check if user is logged in
@auth.route("/")
def home():
    if session.get("user"):
        return jsonify(
            {
                "logged_in": True,
                "user_id": get_current_user_id(session),
                "active_jwt": session["user"]["access_token"],
            }
        )
    return jsonify({"logged_in": False, "user_id": None, "active_jwt": None})


@auth.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True),
        audience=env.get("API_AUDIENCE"),
    )


@auth.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Call back route, accessed after the user has logged in through the auth0 portal
    """
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    if not check_user_in_database():
        register_user()
    if user_info_needs_updating():
        update_user()

    return redirect("/auth/")


@auth.route("/logout")
def logout():
    session.clear()
    url = (
        f"https://{env.get('AUTH0_DOMAIN')}/v2/logout?"
        f"{urlencode({'returnTo': url_for('auth.home', _external=True), 'client_id': env.get('AUTH0_CLIENT_ID')}, quote_via=quote_plus)}"
    )
    return redirect(url)
