from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from website import db
from website.models.queue import Queue

from collections import ChainMap


# COMPONENTS
from website.components.forms.add_user_to_queue import component as add_user_to_queue
from website.components.forms.authorize_user import component as authorize_user
from website.components.forms.register_user import component as register_user

main = Blueprint('main', __name__)


@main.context_processor
def load_components():
    return dict(
        add_user_to_queue=add_user_to_queue,
        authorize_user=authorize_user,
        register_user=register_user
    )

@main.route('/')
def home():
    categories = db.distinct_queue_categories()
    queues = Queue.get(by="active", value=1, getmany=True)
    organized_queues = { category:[] for category in categories }

    for category in categories:
        for queue in queues:
            print (queue.category)
            if queue.category==category:
                organized_queues[category].append(queue)

    return render_template("home.html",
        title="Home",
        organized_queues=organized_queues,
        queues=queues)


@main.route('/test')
def test():
    return render_template('test_qr.html')

@main.route('/qr_code/<string:user_id>/<string:queue_id>')
def temporary_page(user_id, queue_id):
    # create a temporary users table that is wiped out at a particular time
    
    # or, should a jobs section be created? in which temporary processes take place...

    queue_model = Queue.get(by='_id', value=queue_id)
    temp_user = ""
    
    return render_template('temp.html')

@main.route('/queues/<string:queue_id>')
def queue(queue_id):
    queue_model = Queue.get(by='_id', value=queue_id)
    return render_template('queue.html', queue_model=queue_model)


@main.route('/queues/<string:user_id>/<string:queue_id>')
def queue_user_positioned(user_id, queue_id):
    queue_model = Queue.get(by='_id', value=queue_id)
    position = queue_model.get_user_position(user_id)
    return render_template('queue_positioned.html',
            queue_model=queue_model,
            position=position
        )


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

