from flask import Markup, url_for
from website.blueprints.main.forms import Search_Bar


def component():
    form = Search_Bar()
    action = url_for('api.search')
    return Markup(f"""
    <form action="{action}" method="POST">
        <div class="form-group">
            {form.query.label}
            {form.query}
        </div>
        <div class="form-group">
            {form.submit_search_bar}
        </div>
    </form>

    
    
    """)