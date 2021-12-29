from flask import Markup, url_for
from website.blueprints.auth.forms import Authorize_User

def component():
    action = url_for('auth.authorize_user')
    form = Authorize_User()

    return Markup(f"""
    <form method="POST" action="{action}">
        <div class="form-group">
            {form.email.label}
            {form.email}
        </div>
        <div class="form-group">
            {form.password.label}
            {form.password}
        </div>
        <div class="form-group">
            {form.submit_authorize_user}
        </div>
    </form>
    
    """)