from flask import Blueprint

auth = Blueprint("auth", __name__)

from . import errors
from . import routes
