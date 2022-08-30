from flask import send_from_directory

from . import swaggerui_blueprint as docs


@docs.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)
