from flask import Markup, url_for
from website.blueprints.superadmin.forms import Delete_Admin

def component(admin_id):
    action = url_for('superadmin.delete_admin')
    form = Delete_Admin()
    return Markup(f"""
    <form action={action} method='POST'>
        <div class='form_group'>
            {form.admin_id(value=admin_id)}
        </div>
        <div class='form_group'>
            {form.submit_delete_admin}
        </div>
    </form>
    """)