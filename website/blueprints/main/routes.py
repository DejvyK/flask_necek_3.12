from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from website.models.queue import Queue


main = Blueprint('main', __name__)

@main.route('/')
def home():
    active_queue = Queue.get(by="active", value="1")
    if current_user.is_authenticated:
        position = active_queue.get_user_position(current_user._id)
        message = False
    else:
        message = True
        position = active_queue.get_next_opening()

    return render_template("home.html", position=position, message=message)

@main.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated:
        if current_user.admin!=1:
            flash("you don't have access to that page")
            return redirect(url_for('main.home'))

    queues = Queue.get(getall=True)
    return render_template("admin.html", queues=queues)


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

