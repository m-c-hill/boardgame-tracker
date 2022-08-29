from flask import jsonify

from . import auth


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@auth.errorhandler(400)
def resource_not_found(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400


@auth.errorhandler(404)
def resource_not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404


@auth.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
        422,
    )


@auth.errorhandler(500)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 500, "message": "Server side error"}),
        500,
    )


@auth.errorhandler(AuthError)
def unauthorized(error):
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error.get("description"),
            }
        ),
        error.status_code,
    )
