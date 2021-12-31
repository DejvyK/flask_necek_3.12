from flask import Markup, url_for
from website.blueprints.auth.forms import Register_User

def component():
    action = url_for('auth.register_user')
    form = Register_User()

    return Markup(f"""
    <form method="POST" action="{action}">
        <div class="form-group">
            {form.email.label}
            {form.email}
        </div>
        <div class="form-group">
            {form.fname.label}
            {form.fname}
        </div>
        <div class="form-group">
            {form.lname.label}
            {form.lname}
        </div>
        <div class="form-group">
            {form.password.label}
            {form.password}
        </div>
        <div class="form-group">
            {form.confirm_password.label}
            {form.confirm_password}
        </div>
        <div class="form-group">
            {form.admincode.label}
            {form.admincode}
        </div>
        <div class="form-group">
            {form.submit_register_user}
        </div>
    </form>    
    """)