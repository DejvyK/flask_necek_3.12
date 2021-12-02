from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from flask import current_app
import urllib.request 
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
import requests,json ,uuid,pathlib,os

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjsdfsdfhdjah kjshkvsdjdhjs'
    app.config["SQLALCHEMY_DATABASE_URI"]= f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app