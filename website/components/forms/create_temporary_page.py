from flask import Markup, url_for
from website.blueprints.superadmin.forms import Create_Temporary_Page



def component(user_id, queue_id):
    action = url_for('superadmin.create_temporary_page')
    form = Create_Temporary_Page()

    return Markup(f"""
    <form action={action} method='POST'>
        <div class='form_group'>
            {form.user_id.label}
            {form.user_id}
        </div>
        <div class='form_group'>
            {form.queue_id.label}
            {form.queue_id}
        </div>
        <div class='form_group'>
            {form.submit_create_temporary_page}
        </div>
    </form>
    """)