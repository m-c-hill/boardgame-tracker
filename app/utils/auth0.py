import json
from functools import wraps
from os import environ as env
from urllib.request import urlopen

from flask import request, session
from jose import jwt

from ..auth.errors import AuthError

ALGORITHMS = ["RS256"]  # RSA using SHA256
API_AUDIENCE = env.get("API_AUDIENCE")
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")


def get_token_auth_header():
    """
    Retrieve the token from the request auth header
    """
    if "Authorization" not in request.headers:
        raise AuthError(
            {
                "code": "auth_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )

    auth_header = request.headers["Authorization"]
    _validate_bearer_token(auth_header)

    return auth_header.split(" ")[1]


def _validate_bearer_token(header) -> bool:
    """
    Helper function to check if the string 'bearer' preceeds the auth token
    """
    header_parts = header.split(" ")

    if header_parts[0].lower() != "bearer":
        raise AuthError(
            {"code": "invalid_header", "description": "The prefix has to be 'Bearer'."},
            401,
        )

    if len(header_parts) != 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must have the format 'Bearer {{bearer_token}}'.",
            },
            401,
        )

    return True


def check_permissions(permission, payload) -> bool:
    """
    Check the permissions list in the JWT payload contains the required permission.
    """
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "empty_claims",
                "description": "Permissions list not included in JWT",
            },
            401,
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {"code": "unauthorized", "description": "Permission not found"}, 403
        )

    return True


def _retrieve_jwks():
    # auth0 jwks docs: https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-key-sets
    jwks_url = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    return json.loads(jwks_url.read())  # json web key set


def verify_decode_jwt(token) -> bool:
    """
    Decode the jwt token using RSA with SHA256 algorithm
    """

    jwks = _retrieve_jwks()

    # jwt lib docs: https://pyjwt.readthedocs.io/en/stable/usage.html
    unverified_header = jwt.get_unverified_header(token)

    if "kid" not in unverified_header:
        raise AuthError(
            {"code": "invalid_header", "description": "Authorization malformed."}, 401
        )

    # retrieve rsa key used for jtw signature
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "e": key["e"],
                "kid": key["kid"],
                "kty": key["kty"],
                "n": key["n"],
                "use": key["use"],
            }

    # decode the jwt using the rsa key and return the payload
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            return payload

        except jwt.JWTClaimsError:
            raise AuthError(
                {"code": "invalid_claims", "description": "Invalid claims"}, 401
            )

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token has expired"}, 401
            )

        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token",
                },
                400,
            )

    raise AuthError(
        {"code": "invalid_header", "description": "Unable to find rsa key"}, 400
    )


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            # session["user"] = payload
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
