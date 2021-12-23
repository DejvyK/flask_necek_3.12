from flask import Blueprint, jsonify, redirect, url_for, request, flash
from flask_login import login_required, current_user

from website.models.users import User
from website.models.admincode import AdminCode
from website.models.queue import Queue

from secrets import token_hex
import json

api = Blueprint('api', __name__,
    url_prefix='/api')

@api.route('/create_tables', methods=["GET", "POST"])
def create_tables():
    Queue.mk_table()
    return redirect(url_for('main.home'))


@api.route('/add_to_queue', methods=["GET", "POST"])
@login_required
def add_to_queue():
    queue_id = request.form.get("queue_id")
    
    queue = Queue.get(by="_id", value=queue_id)
    result = queue.add_user(current_user._id)

    if result:
        flash("we added you to the queue!")
    else:
        flash ("you're already in the queue")

    return redirect(url_for('main.home'))


@api.route('/leave_queue', methods=["GET", "POST"])
@login_required
def leave_queue():
    queue_id = request.form.get("queue_id")
    user_id = request.form.get("user_id")

    active_queue = Queue.get(by="_id", value=queue_id)
    result = active_queue.remove_user(user_id)
    if result:
        flash("we removed you from the queue!")
    else:
        flash ("something went wrong")
    return redirect(url_for('main.user_queues', user_id=current_user._id))


@api.route('/get_position/<string:user_id>/<string:queue_id>', methods=["GET", "POST"])
def get_position(user_id, queue_id):
    active_queue = Queue.get(by="active", value="1")
    data_list = active_queue.data.split('$')
    position = data_list.index(user_id)
    return position

@api.route('/check_position/<string:user_id>/<string:queue_id>', methods=['GET', 'POST'])
def check_position(user_id, queue_id):
    test = {'test' : 'success'}
    json_file = json.dumps(test)

    queue = Queue.get(by='_id', value=queue_id)

    position = queue.get_user_position(user_id)

    if (position):
        pos = json.dumps({'position' : position})
        return pos, 200
    return test, 400

@api.route('/search', methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    return redirect(url_for('main.search_results', query=query))