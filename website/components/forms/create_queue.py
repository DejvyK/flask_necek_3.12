from flask import Markup, url_for
from website.blueprints.admin.forms import Create_Queue
# from website.models.queue import Queue
from website import db
from website.blueprints.main import unpack_elems

def component():
    action = url_for('admin.create_queue')
    form = Create_Queue()
    categories = db.distinct_queue_categories()

    choices = [f"""
    <option class="form-control" value={category}>
        {category.upper()}
    </option>
    """ for category in categories]


    return Markup(f"""
    <form action="{action}" method="POST">
        
        <div class="form-group">
            {form.title.label}
            {form.title}
        </div>
        <div class="form-group">
            {form.category.label}
            <select name="category">
                {unpack_elems(choices)}
            </select>
        </div>
        <div class="form-group">
            {form.submit_create_queue}
        </div>
        <p>
            creating a new queue will automatically activate it 
        </p>
    </form>
    """)