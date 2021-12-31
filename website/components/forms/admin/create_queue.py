from flask import Markup, url_for
from website.blueprints.admin.forms import Create_Queue

from website import db
from website.blueprints.main import unpack_elems, CATEGORIES

def component():
    action = url_for('admin.create_queue')
    form = Create_Queue()

    choices = [f"""
    <option class="form-control" value={category}>
        {category.upper()}
    </option>
    """ for category in CATEGORIES]


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
    </form>
    """)