from flask_login import UserMixin
from website import login_manager, db


@login_manager.user_loader
def load_user(id):
    auth_model = ""

    return auth_model

class User(UserMixin):
    pass
    # id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(150), unique=True)
    # password = db.Column(db.String(150))
    # krestni = db.Column(db.String(150))
