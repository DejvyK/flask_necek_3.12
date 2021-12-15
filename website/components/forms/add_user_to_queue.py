from flask import Markup, url_for
from flask_login import current_user
from website.blueprints.main.forms import Add_User_To_Queue

def component(queue):
    form = Add_User_To_Queue()
    action = url_for('api.add_to_queue')
    return Markup(f"""
    <form method="POST" action="{action}">
        {form.user_id(value=current_user._id)}
        {form.queue_id(value=queue._id)}
        {form.submit_add_user_to_queue}
        <p>
            Join at position: {queue.get_next_opening()}
        </p>
    </form>
    """)