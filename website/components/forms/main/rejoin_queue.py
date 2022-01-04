from flask import Markup, url_for
from website.blueprints.main.forms import Rejoin_Queue


def component(user_id, queue_id):
    action = url_for('api.rejoin_queue')
    form  = Rejoin_Queue()
    return Markup(f"""
    <form action="{action}" method='POST'>
        <div class='form-group'>
            {form.user_id(value=user_id)}
        </div>
        <div class='form-group'>
            {form.queue_id(value=queue_id)}
        </div>
        <div class='form-group'>
            {form.submit_rejoin_queue}
        </div>
    </form>
    
    """)