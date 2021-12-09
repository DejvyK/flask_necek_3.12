from flask import Blueprint

from website.models.notes import Note
from website.models.users import User


api = Blueprint('api', __name__,
    url_prefix='/api')


@api.route('/create_tables', methods=["GET", "POST"])
def create_tables():
    User.mk_table()
    Note.mk_table()
    return 'run'


@api.route('/get_position', methods=["GET", "POST"])
def get_position():
    pass