from flask import Blueprint

blue = Blueprint('test', __name__)

from . import test_api
