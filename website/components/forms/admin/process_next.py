from flask import Markup, url_for
from website.blueprints.admin.forms import Process_Next

def component(queue):
    action = url_for('admin.process_next')
    form = Process_Next()
    return Markup(f"""
    <form action="{action}" method="POST">
        <div class="form-group">
            {form.queue_id(value=queue._id)}
        </div>
        <div class="form-group">
            {form.submit_process_next}
        </div>
    </form>
    """)