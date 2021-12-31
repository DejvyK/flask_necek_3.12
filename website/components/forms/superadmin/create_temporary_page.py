from flask import Markup, url_for
from website.blueprints.main import unpack_elems
from website.blueprints.superadmin.forms import Create_Temporary_Page
from website.models.queue import Queue

def component(user_id):
    action = url_for('superadmin.create_temporary_page')
    form = Create_Temporary_Page()

    queues = Queue.get(by='active', value='1', getmany=True)

    choices = [f"""
    <option value={queue._id}>
        {queue._id}
    </option>
    """ for queue in queues]

    return Markup(f"""
    <form action={action} method='POST'>
        <div class='form-group'>
            {form.user_id.label}
            {form.user_id(value=user_id)}
        </div>
        
        <div class='form-group'>
            {form.queue_id.label}
            <select name="queue_id">
                {unpack_elems(choices)}
            </select>
        </div>
        
        <div class='form-group'>
            {form.submit_create_temporary_page}
        </div>
    </form>
    """)