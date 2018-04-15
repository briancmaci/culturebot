from flask import Blueprint

api = Blueprint(
    'slack',
    __name__
)

from . import routes