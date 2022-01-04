from flask import Markup, url_for
from website.blueprints.admin.forms import Process_Previous

def component(queue):
    action = url_for('admin.process_previous')
    form = Process_Previous()
    return Markup(f"""
    <form action="{action}" method="POST">
        <div class="form-group">
            {form.queue_id(value=queue._id)}
        </div>
        <div class="form-group">
            {form.submit_process_previous}
        </div>
    </form>
    """)