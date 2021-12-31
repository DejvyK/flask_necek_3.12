from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from website import db
from website.blueprints.main import CATEGORIES
from website.models.queue import Queue


# COMPONENTS
from website.components.forms.main.add_user_to_queue import component as add_user_to_queue
from website.components.forms.main.search_bar import component as search_bar
from website.components.forms.main.leave_queue import component as leave_queue

from website.components.forms.auth.authorize_user import component as authorize_user
from website.components.forms.auth.register_user import component as register_user


main = Blueprint('main', __name__)

@main.context_processor
def load_components():
    return dict(
        add_user_to_queue=add_user_to_queue,
        authorize_user=authorize_user,
        register_user=register_user,
        leave_queue=leave_queue,
        search_bar=search_bar
    )

@main.route('/')
def home():
    queues = Queue.get(getall=True)
    organized_queues = { category:[] for  \
        category in CATEGORIES }

    for category in CATEGORIES:
        for queue in queues:
            if queue.category==category:
                organized_queues[category].append(queue)

    return render_template("home.html",
        title="Home",
        organized_queues=organized_queues,
        )


@main.route('/qr_code/<string:user_id>/<string:queue_id>')
def temporary_page(user_id, queue_id):
    queue = Queue.get(by='_id', value=queue_id)
    temp_user = ""

    position = queue.get_user_position(user_id)
    
    return render_template('temp.html',
        user_id=user_id,
        queue_id=queue_id,
        queue=queue,
        position=position
    )


@main.route('/queues/<string:queue_id>')
def queue(queue_id):
    queue_model = Queue.get(by='_id', value=queue_id)
    return render_template('queue.html', queue_model=queue_model)


@main.route('/user_queues/<string:user_id>')
def user_queues(user_id):
    queue_models = Queue.get(getall=True)
    
    queues = [ queue for queue in queue_models if queue.has_user(user_id) ]

    return render_template('user_queues.html',
            queues=queues,
            user_id=user_id,
        )

@main.route('/queue_positioned/<string:user_id>/<string:queue_id>')
def queue_user_positioned(user_id, queue_id):
    queue = Queue.get(by='_id', value=queue_id)
    position = queue.get_user_position(user_id)
    return render_template('queue_positioned.html',
            queue=queue,
            user_id=user_id,
            position=position
        )


@main.route('/login')
def login():
    if current_user.is_authenticated:
        flash ("You're already logged in, please logout first")
        return redirect(url_for('main.home'))
    return render_template("login.html", title="Login")


@main.route('/search_results/<string:query>')
def search_results(query):
    # 2 ways to do this ajax call:
        #1. loading up all of the models and then unlocking them as we get results from the search
        #2. conduct a search in which the search returns a set of models everytime enter is pressed

        # 2 seems the better route, now, adjust the api to return query models
        # how will the process work? They will usually start their search away from a search page

    # matched_content = []
    # queues = Queue.get(getall=True)

    # for queue in queues:
    #     title_string = str(queue.title)
    #     category_string = str(queue.category)
    #     if distance(title_string, query) < len(title_string) - len(query) + 2 or \
    #         distance(category_string, query) < len(category_string) - len(query) + 2:
    #         matched_content.append(queue)
    return render_template('search_results.html',
        query=query,
        )


@main.route('/sign-up')
def signup():
    if current_user.is_authenticated:
        flash ("You're already logged in, please logout first")
        return redirect(url_for('main.home'))

    return render_template("sign_up.html", title="Signup")

