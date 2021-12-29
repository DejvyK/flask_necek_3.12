from flask import Markup, url_for
from website.blueprints.admin.forms import Delete_Queue

def component(queue):
    action = url_for('admin.delete_queue')
    form = Delete_Queue()

    return Markup(f"""
    <form method="POST" action={action}>
        <div class="form-group">
            {form.queue_id(value=queue._id)}
        </div>
        <div class="form-group">
            {form.submit_delete_queue}
        </div>
    </form>    
    """)
