from flask import url_for, session, redirect
from urllib.parse import quote_plus, urlencode
from os import environ as env

from . import auth

from app import oauth
from ..models.user import User

@auth.route("/")
def home():
    user = session.get("user")
    return f"current jwt: {user}"


@auth.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True)
    )


@auth.route("/callback", methods=["GET", "POST"])
def callback():
    # TODO: check if user just registered
    #   If they did, store the new user information
    #

    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/auth/")


@auth.route("/logout")
def logout():
    session.clear()
    url = (
        f"https://{env.get('AUTH0_DOMAIN')}/v2/logout?"
        f"{urlencode({'returnTo': url_for('auth.home', _external=True), 'client_id': env.get('AUTH0_CLIENT_ID')}, quote_via=quote_plus)}"
    )
    return redirect(url)


@auth.route("/register")
def register():
    return
