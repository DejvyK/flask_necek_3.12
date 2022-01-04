from flask import Blueprint, jsonify, redirect, url_for, request, flash
from flask_login import login_required, current_user

from Levenshtein import distance
from secrets import token_hex
import json


from website.models.users import User
from website.models.admincode import AdminCode
from website.models.queue import Queue


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

    queue = Queue.get(by="_id", value=queue_id)

    queue.skip_users += f"{user_id}$"

    try:
        Queue.update(queue)
        flash("we removed you from the queue!")
    except Exception as err:        
        print (err)
        flash ("something went wrong")

    return redirect(url_for('main.user_queues', user_id=current_user._id))



@api.route('/rejoin_queue', methods=['GET', 'POST'])
@login_required
def rejoin_queue():
    user_id = request.form.get('user_id')
    queue_id = request.form.get('queue_id')

    queue = Queue.get(by='_id', value=queue_id)

    # check if the user is already passed, then put them at the end of the queue

    

    if queue.has_skipped(user_id):
        if queue.check_skipped(user_id):
            
            flash ("they've already called for your line, we have to")


    #     queue.remove_skipped(user_id)




    return redirect(url_for('main.user_queues', user_id=user_id))
@api.route('/get_position/<string:user_id>/<string:queue_id>', methods=["GET", "POST"])
def get_position(user_id, queue_id):
    active_queue = Queue.get(by="active", value="1")
    data_list = active_queue.data.split('$')
    position = data_list.index(user_id)
    return position

@api.route('/check_position/<string:user_id>/<string:queue_id>', methods=['GET', 'POST'])
def check_position(user_id, queue_id):
    queue = Queue.get(by='_id', value=queue_id)

    position = queue.get_user_position(user_id)

    if (position):
        pos = json.dumps({'position' : position})
        return pos, 200

    fail = {'status' : 'failed'}
    json_fail = json.dumps(fail)
    
    return json_fail, 400

# @api.route('/search', methods=["GET", "POST"])
# def search():
#     query = request.form.get("query")


#     return redirect(url_for('main.search_results', query=query))


@api.route('/search/<string:query>', methods=["GET", "POST"])
def search(query):
    matched_content = []
    queues = Queue.get(getall=True)

    for queue in queues:
        title_string = str(queue.title)
        category_string = str(queue.category)
        if distance(title_string, query) < len(title_string) - len(query) + 2 or \
            distance(category_string, query) < len(category_string) - len(query) + 2:
            matched_content.append(queue)

    if (matched_content):
        models_as_dict = [model.as_dict for model in matched_content if model]
        models_as_json = json.dumps(models_as_dict)
        return models_as_json, 200

    fail = {'status' : 'failed'}
    json_fail = json.dumps(fail)
    
    return json_fail, 400