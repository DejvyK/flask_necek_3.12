from flask import Blueprint, request, redirect, url_for
from flask_login import current_user, login_required
from website.models.queue import Queue

admin = Blueprint('admin', __name__,
    url_prefix='/admin')

@admin.route('/create_queue')
@login_required
def create_queue():
    mdict = {
        'data' : "",
        'active' : 1,
        'user_id' : current_user._id
    }
    new_queue = Queue(mdict)
    admin_active_queue = Queue.get_active_admin_queue(current_user._id)

    try:
        Queue.add(new_queue)
        if (admin_active_queue):
            admin_active_queue.active = 0
            Queue.update(admin_active_queue)
    except Exception as err:
        print (err)
        flash ("error adding new queue")

    finally:
        return redirect(url_for('main.admin'))


@admin.route('/delete_queue', methods=['POST', 'GET'])
@login_required
def delete_queue():
    queue_id = request.form.get("queue_id")
    
    queue = Queue.get(by='_id', value=queue_id)

    print(queue_id)
    # new_queue = Queue(mdict)
    # admin_active_queue = Queue.get_active_admin_queue(current_user._id)

    try:
        pass
        # Queue.add(new_queue)
        # if (admin_active_queue):
            # admin_active_queue.active = 0
            # Queue.update(admin_active_queue)
    except Exception as err:
        pass
        # print (err)
        # flash ("error adding new queue")

    finally:
        # pass
        return redirect(url_for('main.admin'))

@admin.route('/reactivate_queue', methods=['POST', 'GET'])
@login_required
def reactivate_queue():
    queue_id = request.form.get("queue_id")
    
    queue = Queue.get(by='_id', value=queue_id)
    admin_active_queue = Queue.get_active_admin_queue(current_user._id)


    queue.active = 1
    admin_active_queue.active = 0

    print (admin_active_queue)
    print (queue)

    try:
        # Queue.update(admin_active_queue)
        # Queue.update(queue)
        Flash ('successfully update')
        # Queue.add(new_queue)
        # if (admin_active_queue):
            # admin_active_queue.active = 0
            # Queue.update(admin_active_queue)
    except Exception as err:
        print (err)
        Flash ('something went wrong')
        # print (err)
        # flash ("error adding new queue")
    finally:
        # pass
        return redirect(url_for('main.admin'))


