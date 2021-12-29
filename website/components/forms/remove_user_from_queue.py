from flask import Markup, url_for
from website.blueprints.admin.forms import Remove_User_From_Queue

def component(queue_id, user_id):
    form = Remove_User_From_Queue()
    action = url_for('admin.remove_user_from_queue')
    return Markup(f"""
    <form method="POST" action="{action}">
        <div class="form-group">
            {form.queue_id(value=queue_id)}
        </div>
        <div class="form-group">
            {form.user_id(value=user_id)}
        </div>
        <div class="form-group">
            {form.submit_remove_user}
        </div>
    </form>
    """)