from flask import Blueprint, jsonify, redirect, url_for, request, flash

from website.models.notes import Note
from website.models.users import User
from website.models.admincode import AdminCode
from website.models.queue import Queue

from secrets import token_hex

api = Blueprint('api', __name__,
    url_prefix='/api')

@api.route('/create_tables', methods=["GET", "POST"])
def create_tables():
    Queue.mk_table()
    return redirect(url_for('main.home'))

@api.route('/add_to_queue', methods=["GET", "POST"])
def add_to_queue():
    user_id = request.form.get("user_id")
    queue_id = request.form.get("queue_id")
    
    queue = Queue.get(by="_id", value=queue_id)
    result = queue.add_user(user_id)

    if result:
        flash("we added you to the queue!")
    else:
        flash ("you're already in the queue")

    return redirect(url_for('main.home'))


@api.route('/remove_from_queue/<string:user_id>', methods=["GET", "POST"])
def remove_from_queue(user_id):
    active_queue = Queue.get(by="active", value="1")
    result = active_queue.remove_user(user_id)
    if result:
        flash("we removed you to the queue!")
    else:
        flash ("something went wrong")

    return redirect(url_for('main.admin'))



@api.route('/get_position/<string:user_id>', methods=["GET", "POST"])
def get_position(user_id):
    active_queue = Queue.get(by="active", value="1")
    data_list = active_queue.data.split('$')
    position = data_list.index(user_id)
    return position









# @api.route('/add_admincode>', methods=["GET", "POST"])
# def add_admincode():
#     # code = token_hex(4)
#     mdict = {
#         'code' : code
#     }

#     new_code = AdminCode(mdict)

#     try:
#         AdminCode.add(new_code)
#         return jsonify({'status' : 'successful'})
#     except Exception as err:
#         print(err)
#         return jsonify({'status' : 'error'})