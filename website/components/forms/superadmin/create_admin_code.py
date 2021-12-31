from flask import Markup, url_for
from website.blueprints.superadmin.forms import Create_Admin_Code

def component():
    form = Create_Admin_Code()
    action = url_for('superadmin.create_admin_code')
    return Markup(f"""
    <form action={action} method="POST">
        <div class="form_group">
            {form.code.label}
            {form.code}
        </div>
        <div class="form_group">
            {form.submit_admin_code}
        </div>
    </form>
    """)