from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from website.models.queue import Queue
from website.models.users import User

# COMPONENTS
from website.components.forms.admin.create_queue import component as create_queue_form
from website.components.forms.admin.delete_queue import component as delete_queue_form
from website.components.forms.admin.process_next import component as process_next_form
from website.components.forms.admin.process_previous import component as process_previous_form
from website.components.forms.main.search_bar import component as search_bar

admin = Blueprint('admin', __name__,
    url_prefix='/admin')

@admin.context_processor
def load_components():
    return dict(
        create_queue_form=create_queue_form,
        delete_queue_form=delete_queue_form,
        process_next_form=process_next_form,
        process_previous_form=process_previous_form,
        search_bar=search_bar,
    )


@admin.route('/')
@login_required
def home():
    if current_user.is_authenticated:
        if current_user.admin!=1:
            flash("you don't have access to that page")
            return redirect(url_for('main.home'))

    queue = Queue.get(by="user_id", value=current_user._id)

    if queue:
        processing_user = queue.get_processing_user()
    else:
        processing_user = False

    return render_template("admin.html",
        title="Admin",
        processing_user=processing_user,
        queue=queue
        )


@admin.route('/create_queue', methods=['POST', 'GET'])
@login_required
def create_queue():
    if request.method=='POST':            
        mdict = {
            'user_id' : current_user._id,
            'data' : '',
            'category' : request.form.get('category'),
            'title' : request.form.get('title'),
            'processing' : 0,
            'skip_users' : '',
        }
        new_queue = Queue(mdict)

        try:
            Queue.add(new_queue)
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


@admin.route('/process_previous', methods=['GET', 'POST'])
@login_required
def process_previous():
    queue_id = request.form.get("queue_id")

    queue = Queue.get(by="_id", value=queue_id)
    
    if queue.processing > 0:
        queue.processing -= 1
        # next_user_id = queue.data_as_list[queue.processing]

        skip = True
        while skip:
            next_user_id = queue.data_as_list[queue.processing]
            if queue.has_skipped(next_user_id):
                queue.processing -= 1
            else:
                skip = False
                # break
        try:
            Queue.update(queue)
            flash ('updated')
        except Exception as err:
            print (err)
            flash ('something went wrong')
    else:
        flash ("you're already at the beginning of the queue")

    return redirect(url_for('admin.home'))


@admin.route('/process_next', methods=['GET', 'POST'])
@login_required
def process_next():
    queue_id = request.form.get("queue_id")

    queue = Queue.get(by="_id", value=queue_id)

    if queue.processing >= 0 and queue.processing < len(queue.data_as_list):
        queue.processing += 1

        skip = True
        while skip:
            try:
                next_user_id = queue.data_as_list[queue.processing]
            except Exception as err:
                print (err)
                break
            if queue.has_skipped(next_user_id):
                queue.processing += 1
            else:
                skip = False
                # break

        if queue.processing >= 0 and queue.processing < len(queue.data_as_list):
            try:
                Queue.update(queue)
                flash ('updated')
            except Exception as err:
                print (err)
                flash ('something went wrong')
        else:
            pass

    else:
        flash ("you're already at the end of the queue")

    return redirect(url_for('admin.home'))