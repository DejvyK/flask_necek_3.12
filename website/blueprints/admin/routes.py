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
    }
    new_queue = Queue(mdict)
    try:
        Queue.add(new_queue)
    except Exception as err:
        print (err)
        flash ("error adding new queue")

    finally:
        return redirect(url_for('main.admin'))



