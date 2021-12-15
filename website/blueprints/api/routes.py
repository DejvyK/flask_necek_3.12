from flask import Blueprint, jsonify, redirect, url_for, request, flash
from flask_login import login_required, current_user
from website.models.notes import Note
from website.models.users import User
from website.models.admincode import AdminCode
from website.models.queue import Queue

from secrets import token_hex
import json

# even if temp_user doesn't have an account
# add user to queue (end) with qr-code
# super-user, can print a ticket (qr code on the ticket)
# join queue through qr code
# webpage will show exact position

# active-queues after midnight are reset, 
# deactivated queues are deleted


# add search bar for cats (last)

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

# one user sends 
@api.route('/remove_from_queue/<string:user_id>/<string:queue_id>', methods=["GET", "POST"])
def remove_from_queue(user_id, queue_id):
    active_queue = Queue.get(by="_id", value=queue_id)
    result = active_queue.remove_user(user_id)
    if result:
        flash("we removed you from the queue!")
    else:
        flash ("something went wrong")

    return redirect(url_for('admin.home'))


@api.route('/get_position/<string:user_id>', methods=["GET", "POST"])
def get_position(user_id):
    active_queue = Queue.get(by="active", value="1")
    data_list = active_queue.data.split('$')
    position = data_list.index(user_id)
    return position

@api.route('/check_position')
def check_position():
    # return json of position
    test = {'test' : 'success'}

    return json.dumps(test)
