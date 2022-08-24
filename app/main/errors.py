from flask import jsonify

from . import main


@main.errorhandler(400)
def resource_not_found(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400


@main.errorhandler(404)
def resource_not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404


@main.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
        422,
    )


@main.errorhandler(500)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 500, "message": "Server side error"}),
        500,
    )
