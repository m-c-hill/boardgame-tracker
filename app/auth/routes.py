# TODO - https://realpython.com/token-based-authentication-with-flask/#route-setup

from flask import url_for, session, redirect
from urllib.parse import quote_plus, urlencode
from os import environ as env
import json

from . import auth

from app import oauth


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