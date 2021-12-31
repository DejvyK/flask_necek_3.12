from flask import Markup, url_for
from website.blueprints.superadmin.forms import Create_Temporary_User
from secrets import token_hex

def component():
    action = url_for('superadmin.create_temporary_user')
    form = Create_Temporary_User()

    token = token_hex(6)

    return Markup(f"""
    <form action={action} method='POST'>
        <div class='form_group'>
            {form.user_id.label}
            {form.user_id(value=token)}
        </div>
        <div class='form_group'>
            {form.submit_create_temporary_user}
        </div>
    </form>
    """)