from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_qrcode import QRcode

from website.configs import Config
from website.db import DB

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"

bcrypt = Bcrypt()
db = DB()
qrcode = QRcode()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    db.init_app(app)
    qrcode.init_app(app)
    login_manager.init_app(app)

    from website.blueprints.\
        main.routes import main

    from website.blueprints.\
        api.routes import api

    from website.blueprints.\
        auth.routes import auth

    from website.blueprints.\
        admin.routes import admin

    from website.blueprints.\
        superadmin.routes import superadmin

    from website.blueprints.\
        errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(superadmin)
    # app.register_blueprint(errors)

    return app