from flask import jsonify


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def register_error_handlers(app):
    @app.errorhandler(AuthError)
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

    @app.errorhandler(400)
    def resource_not_found(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Server side error"}),
            500,
        )

    @app.after_request
    def after_request(response):
        """
        When a request is received, run this method to add additional CORS headers to the response.
        """
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response
