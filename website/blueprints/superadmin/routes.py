from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required

from website.models.queue import Queue
from website.models.admincode import AdminCode
from website.models.users import User

from website.components.forms.create_admin_code import component as create_admin_code_form
from website.components.forms.delete_admin import component as delete_admin_form
from website.components.forms.create_temporary_page import component as create_temporary_page_form
from website.components.forms.create_temporary_user import component as create_temporary_user_form
# from website.components.forms.create_temporary_page import component as create_temporary_page_form
from website.components.forms.search_bar import component as search_bar


superadmin = Blueprint('superadmin', __name__,
    url_prefix='/superadmin')


@superadmin.context_processor
def load_components():
    return dict(
        search_bar=search_bar,
        create_admin_code_form=create_admin_code_form,
        delete_admin_form=delete_admin_form,
        create_temporary_page_form=create_temporary_page_form,
        create_temporary_user_form=create_temporary_user_form
    )

@superadmin.route('/')
@login_required
def home():
    active_queues = Queue.get(by='active', value=1)

    all_users = User.get(getall=True)
    temps = []
    admins = []
    verified = []

    for user in all_users:
        if user.admin == 0:
            verified.append(user)
        elif user.admin == 1:
            admins.append(user)
        elif user.admin == 3:
            temps.append(user)

    if current_user.is_authenticated:
        if current_user.admin != 2:
            flash ("you don't have access to that page")
            return redirect(url_for('main.home'))

    return render_template('superadmin.html',
        admins=admins,
        temps=temps,
        verified=verified,
        active_queues=active_queues
        )



@superadmin.route('/create_admin_code', methods=['GET', 'POST'])
@login_required
def create_admin_code():
    code = request.form.get("code")
    mdict = {
        'code': code
    }
    new_code = AdminCode(mdict)
    try:
        AdminCode.add(new_code)
        flash ("Successfully created new admin code")
    except Exception as err:
        print (err)
        flash ("There was an error creating your new admin code")

    finally:
        return(redirect(url_for('superadmin.home')))


@superadmin.route('/delete_admin', methods=['GET', 'POST'])
@login_required
def delete_admin():
    admin_id = request.form.get('admin_id')
    admin = User.get(by='_id', value=admin_id)
    admin_queues = Queue.get(by='user_id', value=admin_id, getmany=True)

    try:
        for queue in admin_queues:
            Queue.remove(queue)
        User.remove(admin)
        flash ("successfully deleted admin and their queues")
    except Exception as err:
        flash ("error, could not delete admin")
        print (err)

    finally:
        return(redirect(url_for('superadmin.home')))


@superadmin.route('/create_temporary_page', methods=['GET', 'POST'])
@login_required
def create_temporary_page():
    user_id = request.form.get('user_id')
    queue_id = request.form.get('queue_id')
    print (queue_id)

    queue = Queue.get(by="_id", value=queue_id)
    result = queue.add_user(user_id)
    # result = False

    if result:
        flash ("we added the user to the queue")
    else:
        flash ("you're already in the queue")

    return redirect(url_for('superadmin.home'))




@superadmin.route('/create_temporary_user', methods=['GET', 'POST'])
@login_required
def create_temporary_user():
    user_id = request.form.get('user_id')

    mdict = {
        '_id' : user_id,
        'email' : user_id,
        'fname' : 'temporary',
        'lname' : 'temporary',
        'password' : user_id,
        'admin' : 3,
    }

    new_user = User(mdict)

    try:
        User.add(new_user)
        next_page = request.args.get('next')
        flash ('successful!')
    except Exception as err:
        print(err)
        flash ('something went wrong!')

    finally:
        return redirect(url_for('superadmin.home'))