from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from website.models.queue import Queue


main = Blueprint('main', __name__)

@main.route('/')
def home():
    position = 0
    message = True
    queues = Queue.get(by="active", value="1", getmany=True)

    return render_template("home.html",
        title="Home",
        queues=queues,
        position=position,
        message=message)

@main.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated:
        if current_user.admin!=1:
            flash("you don't have access to that page")
            return redirect(url_for('main.home'))

    queues = Queue.get(by="user_id", value=current_user._id, getmany=True)

    active_queue = ""
    inactive_queues = []

    for queue in queues:
        if (queue.active):
            active_queue = queue
        else:
            inactive_queues.append(queue)

    return render_template("admin.html",
        title="Admin",
        active_queue=active_queue,
        inactive_queues=inactive_queues)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash ("You're already logged in, please logout first")
        return redirect(url_for('main.home'))

    return render_template("login.html", title="Login")

@main.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash ("You're already logged in, please logout first")
        return redirect(url_for('main.home'))

    return render_template("sign_up.html", title="Signup")

