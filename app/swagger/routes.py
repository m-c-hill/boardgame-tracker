from flask import send_from_directory

from . import swaggerui_blueprint as docs


@docs.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@docs.route("/")
def welcome():
    return "Welcome to Board Game Tracker API. Please visit /auth/login to create an account. Then view the documentation at /swagger to get started using the API."
