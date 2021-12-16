from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from website.models.queue import Queue


# COMPONENTS
from website.components.forms.create_queue import component as create_queue_form
from website.components.forms.delete_queue import component as delete_queue_form
from website.components.forms.reactivate_queue import component as reactivate_queue_form
from website.components.forms.search_bar import component as search_bar
from website.components.forms.remove_user_from_queue import component as remove_user_from_queue_form

admin = Blueprint('admin', __name__,
    url_prefix='/admin')

@admin.context_processor
def load_components():
    return dict(
        create_queue_form=create_queue_form,
        delete_queue_form=delete_queue_form,
        reactivate_queue_form=reactivate_queue_form,
        search_bar=search_bar,
        remove_user_from_queue_form=remove_user_from_queue_form,
    )


@admin.route('/')
@login_required
def home():
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


@admin.route('/create_queue', methods=['POST', 'GET'])
@login_required
def create_queue():
    if request.method=='POST':            
        mdict = {
            'data' : '',
            'active' : 1,
            'category' : request.form.get('category'),
            'title' : request.form.get('title'),
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
            return redirect(url_for('admin.home'))


@admin.route('/delete_queue', methods=['POST', 'GET'])
@login_required
def delete_queue():
    queue_id = request.form.get("queue_id")
    
    queue = Queue.get(by='_id', value=queue_id)
    print(queue_id)
    try:
        Queue.remove(queue)
        flash ("successfully delete the queue!")
    except Exception as err:
        print (err)
        flash ("could not delete the queue")

    finally:
        return redirect(url_for('admin.home'))

@admin.route('/reactivate_queue', methods=['POST', 'GET'])
@login_required
def reactivate_queue():
    queue_id = request.form.get("queue_id")
    
    queue = Queue.get(by='_id', value=queue_id)
    admin_active_queue = Queue.get_active_admin_queue(current_user._id)


    print (queue._id)
    print (queue.admin_active_queue)

    try:
        queue.active = 1
        if (admin_active_queue):
            admin_active_queue.active = 0
        flash ('successfully update')
    except Exception as err:
        print (err)
        flash ('something went wrong')
    finally:
        return redirect(url_for('admin.home'))



@admin.route('/remove_user_from_queue', methods=["GET", "POST"])
@login_required
def remove_user_from_queue():
    queue_id = request.form.get("queue_id")
    user_id = request.form.get("user_id")

    active_queue = Queue.get(by="_id", value=queue_id)
    result = active_queue.remove_user(user_id)
    if result:
        flash("we removed you from the queue!")
    else:
        flash ("something went wrong")

    return redirect(url_for('admin.home'))
