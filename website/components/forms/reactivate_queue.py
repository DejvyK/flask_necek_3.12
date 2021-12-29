from flask import Markup, url_for
from website.blueprints.admin.forms import Reactivate_Queue

def component(queue):
    action = url_for('admin.reactivate_queue')
    form = Reactivate_Queue()

    return Markup(f"""
    <form method="POST" action={action}>
        <div class="form-group">
            {form.queue_id(value=queue._id)}
        </div>
        <div class="form-group">
            {form.submit_reactivate_queue}
        </div>
    </form>
    """)
