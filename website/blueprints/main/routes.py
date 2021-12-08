from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("home.html")


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash ("You're already logged in, please logout first")
        return redirect(url_for('main.home'))

    return render_template("login.html")

@main.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash ("You're already logged in, please logout first")
        return redirect(url_for('main.home'))

    return render_template("sign_up.html")

